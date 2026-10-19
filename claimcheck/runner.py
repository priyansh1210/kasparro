"""Sequential evaluation runs over a fixed CSV split, persisted to PostgreSQL and saved
as local report files under runs/."""
from __future__ import annotations

import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from . import db
from .agent import AGENT_VERSIONS, prompt_hash, run_agent
from .config import (DATASET_VERSION, EVALUATOR_VERSION, FACT_VERSION, ROOT, RUNS_DIR,
                     get_settings)
from .data import file_hashes, load_answers, load_gold
from .providers import Provider, build_provider
from .scoring import AnswerOutcome, score

SPLITS = ("development", "check")


def source_hash() -> str:
    """SHA-256 over agent code, prompts and schema: the 'frozen version' fingerprint."""
    h = hashlib.sha256()
    files = sorted((ROOT / "claimcheck").glob("*.py")) + sorted((ROOT / "prompts").glob("*.md"))
    for p in files:
        h.update(p.relative_to(ROOT).as_posix().encode())
        h.update(p.read_bytes().replace(b"\r\n", b"\n"))
    return h.hexdigest()


def source_revision() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def run_metadata(version: str, split: str, provider: Provider) -> dict:
    settings = get_settings()
    return {
        "split": split, "agent_version": version, "prompt_file": AGENT_VERSIONS[version]["prompt"],
        "prompt_hash": prompt_hash(version), "source_hash": source_hash(),
        "source_revision": source_revision(), "dataset_version": DATASET_VERSION,
        "evaluator_version": EVALUATOR_VERSION, "fact_version": FACT_VERSION,
        "provider": provider.name, "model": provider.model,
        "settings": {**settings.public(), "output_mode": AGENT_VERSIONS[version]["mode"]},
        "file_hashes": file_hashes(),
    }


def evaluate(version: str, split: str, provider: Provider | None = None, database_url: str | None = None,
             answer_ids: list[str] | None = None, write_files: bool = True, log=print,
             workers: int = 1) -> dict:
    if split not in SPLITS:
        raise ValueError(f"split must be one of {SPLITS}")
    if version not in AGENT_VERSIONS:
        raise ValueError("agent_version must be v1 or v2")
    provider = provider or build_provider(get_settings())
    answers = [a for a in load_answers() if a.split == split]
    if answer_ids:
        answers = [a for a in answers if a.answer_id in set(answer_ids)]
    gold = load_gold() if split == "development" else None
    meta = run_metadata(version, split, provider)
    meta["settings"]["workers"] = workers
    started = datetime.now(timezone.utc)

    with db.connect(database_url) as conn:
        run_id = db.create_run(conn, meta)
        out_dir = RUNS_DIR / f"{started:%Y%m%dT%H%M%S}_{version}_{split}_{str(run_id)[:8]}"
        results = []
        try:
            # Agent calls may run in a small thread pool (workers=1 is fully sequential).
            # Database writes stay on this thread; answer rows keep their CSV order via seq.
            with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
                futures = {pool.submit(run_agent, a, version, provider): (seq, a) for seq, a in enumerate(answers)}
                by_seq = {}
                for fut in as_completed(futures):
                    seq, answer = futures[fut]
                    res = fut.result()
                    if write_files:
                        trace_path = out_dir / "traces" / f"{answer.answer_id}.json"
                        trace_path.parent.mkdir(parents=True, exist_ok=True)
                        trace_path.write_text(json.dumps({"answer_id": answer.answer_id, "status": res.status,
                                                          "error_type": res.error_type, "exchange": res.trace},
                                                         indent=1, ensure_ascii=False), encoding="utf-8")
                        res.trace_ref = trace_path.relative_to(ROOT).as_posix()
                    db.insert_answer(conn, run_id, seq, res, None)
                    by_seq[seq] = res
                    log(f"[{version}/{split}] {answer.answer_id} {res.status} claims={len(res.claims)} "
                        f"turns={res.turns} {res.latency_ms}ms {res.error_type or ''}")
            results = [by_seq[i] for i in range(len(answers))]
            outcomes = [AnswerOutcome(r.answer_id, r.status, r.claims, r.error_type) for r in results]
            summary = score([a.answer_id for a in answers], outcomes,
                            {a.answer_id: a.ai_answer for a in answers}, gold)
            if summary.get("matches"):
                db.update_matches(conn, run_id, summary["matches"])
            db.finish_run(conn, run_id, "completed", summary)
            status = "completed"
        except BaseException as exc:  # interrupted / infrastructure failure: keep partial evidence
            conn.rollback()
            db.finish_run(conn, run_id, "failed", None, failure_reason=type(exc).__name__)
            raise

    report = {"run_id": str(run_id), "status": status, "metadata": meta,
              "started_at": started.isoformat(), "finished_at": datetime.now(timezone.utc).isoformat(),
              "summary": {k: v for k, v in summary.items() if k != "matches"},
              "answers": [{"answer_id": r.answer_id, "status": r.status, "error_type": r.error_type,
                           "error_message": r.error_message, "turns": r.turns, "latency_ms": r.latency_ms,
                           "trace_ref": getattr(r, "trace_ref", None),
                           "claims": [{**c, **({"match": summary["matches"].get(c["claim_id"])}
                                              if summary.get("matches") is not None else {})}
                                      for c in r.claims]}
                          for r in results]}
    if write_files:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
        (out_dir / "report.md").write_text(render_markdown(report, gold, answers), encoding="utf-8")
        report["report_dir"] = out_dir.relative_to(ROOT).as_posix()
    return report


def render_markdown(report: dict, gold, answers) -> str:
    s, m = report["summary"], report["metadata"]
    lines = [f"# Run {report['run_id']} ({m['agent_version']} / {m['split']})", "",
             f"- status: {report['status']}", f"- provider/model: {m['provider']} / {m['model']}",
             f"- settings: `{json.dumps(m['settings'])}`",
             f"- prompt_hash: `{m['prompt_hash']}`", f"- source_hash: `{m['source_hash']}`",
             f"- versions: dataset {m['dataset_version']}, facts {m['fact_version']}, evaluator {m['evaluator_version']}",
             f"- file hashes: `{json.dumps(m['file_hashes'])}`",
             f"- started {report['started_at']} finished {report['finished_at']}", "",
             "## Counts", "",
             f"answers scheduled {s['answers_scheduled']}, ok {s['answers_ok']}, error {s['answers_error']} "
             f"{s['error_counts']}, empty {s['answers_empty']}; G={s['G']} P={s['P']} M={s['M']} C={s['C']}", ""]
    if s["metrics"]:
        e, j = s["metrics"]["extraction"], s["metrics"]["joint"]
        lines += ["## Metrics", "", "| | precision | recall | F1 |", "|---|---|---|---|",
                  f"| extraction | {e['precision']:.4f} | {e['recall']:.4f} | {e['f1']:.4f} |",
                  f"| joint (main) | {j['precision']:.4f} | {j['recall']:.4f} | {j['f1']:.4f} |", "",
                  f"coverage C/G = {s['metrics']['coverage']:.4f}", ""]
    else:
        lines += ["Quality metrics: null (check split; scored privately by reviewers).", ""]
    if gold is not None:
        gmap = {g.claim_id: g for g in gold}
        pred = {c["claim_id"]: c for a in report["answers"] for c in a["claims"]}
        lines += ["## Missed gold claims", ""] + [
            f"- `{gid}` [{gmap[gid].expected_label}] {gmap[gid].quote}" for gid in s["missed_gold_ids"]] + [""]
        lines += ["## Extra (unmatched) predictions", ""] + [
            f"- `{pid}` [{pred[pid]['label']}] {pred[pid]['quote']}" for pid in s["unmatched_prediction_ids"]] + [""]
        lines += ["## Wrong labels", ""] + [
            f"- `{pid}` predicted {pred[pid]['label']}, expected {pred[pid]['match']['gold_label']}: "
            f"{pred[pid]['quote']} -- reason: {pred[pid]['reason']}" for pid in s["wrong_label_ids"]] + [""]
    lines += ["## Answer outcomes", "", "| answer | status | claims | turns | latency ms | error |",
              "|---|---|---|---|---|---|"]
    for a in report["answers"]:
        lines.append(f"| {a['answer_id']} | {a['status']} | {len(a['claims'])} | {a['turns']} | "
                     f"{a['latency_ms']} | {a['error_type'] or ''} {a['error_message'] or ''} |")
    lines += ["", "## Predictions", ""]
    for a in report["answers"]:
        for c in a["claims"]:
            lines.append(f"- `{c['claim_id']}` **{c['label']}** {c['fact_ids']} {c['quote']} -- {c['reason']}")
    return "\n".join(lines) + "\n"
