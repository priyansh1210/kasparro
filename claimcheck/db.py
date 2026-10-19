"""PostgreSQL persistence with psycopg 3. All SQL is parameterized."""
from __future__ import annotations

import uuid
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from .config import ROOT, get_settings


@contextmanager
def connect(database_url: str | None = None):
    url = database_url or get_settings().database_url
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    with psycopg.connect(url, row_factory=dict_row, connect_timeout=10) as conn:
        yield conn


def init_schema(database_url: str | None = None) -> None:
    sql = (ROOT / "sql" / "schema.sql").read_text(encoding="utf-8")
    with connect(database_url) as conn:
        conn.execute(sql)


def create_run(conn, meta: dict) -> uuid.UUID:
    run_id = uuid.uuid4()
    conn.execute(
        """INSERT INTO runs (id, split, agent_version, prompt_hash, source_hash, source_revision,
               dataset_version, evaluator_version, fact_version, provider, model, settings,
               file_hashes, status)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'running')""",
        (run_id, meta["split"], meta["agent_version"], meta["prompt_hash"], meta["source_hash"],
         meta.get("source_revision"), meta["dataset_version"], meta["evaluator_version"],
         meta["fact_version"], meta["provider"], meta["model"], Jsonb(meta["settings"]),
         Jsonb(meta["file_hashes"])),
    )
    conn.commit()
    return run_id


def insert_answer(conn, run_id, seq: int, result, matches: dict | None) -> None:
    """One terminal answer row plus its accepted claims, in one transaction."""
    with conn.transaction():
        conn.execute(
            """INSERT INTO answer_results (run_id, answer_id, seq, status, error_type, error_message,
                   claim_count, turns, latency_ms, trace_ref)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (run_id, result.answer_id, seq, result.status, result.error_type, result.error_message,
             len(result.claims), result.turns, result.latency_ms, getattr(result, "trace_ref", None)),
        )
        for c in result.claims:
            m = (matches or {}).get(c["claim_id"]) or {}
            conn.execute(
                """INSERT INTO claim_results (run_id, answer_id, claim_id, start_char, end_char, quote,
                       label, fact_ids, reason, matched_gold_id, gold_label, label_correct)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (run_id, result.answer_id, c["claim_id"], c["start_char"], c["end_char"], c["quote"],
                 c["label"], Jsonb(c["fact_ids"]), c["reason"], m.get("gold_claim_id"),
                 m.get("gold_label"), m.get("label_correct")),
            )


def update_matches(conn, run_id, matches: dict) -> None:
    with conn.transaction():
        for claim_id, m in matches.items():
            conn.execute(
                """UPDATE claim_results SET matched_gold_id = %s, gold_label = %s, label_correct = %s
                   WHERE run_id = %s AND claim_id = %s""",
                (m["gold_claim_id"], m["gold_label"], m["label_correct"], run_id, claim_id),
            )


def finish_run(conn, run_id, status: str, summary: dict | None, failure_reason: str | None = None) -> None:
    summary = summary or {}
    counts = {k: summary.get(k) for k in ("answers_scheduled", "answers_ok", "answers_error",
                                          "answers_empty", "error_counts", "G", "P", "M", "C")} if summary else None
    conn.execute(
        """UPDATE runs SET status = %s, failure_reason = %s, counts = %s, metrics = %s,
               missed_gold_ids = %s, unmatched_prediction_ids = %s, wrong_label_ids = %s,
               finished_at = now()
           WHERE id = %s""",
        (status, failure_reason, Jsonb(counts) if counts else None,
         Jsonb(summary["metrics"]) if summary.get("metrics") is not None else None,
         Jsonb(summary["missed_gold_ids"]) if summary.get("missed_gold_ids") is not None else None,
         Jsonb(summary["unmatched_prediction_ids"]) if summary.get("unmatched_prediction_ids") is not None else None,
         Jsonb(summary["wrong_label_ids"]) if summary.get("wrong_label_ids") is not None else None,
         run_id),
    )
    conn.commit()


def get_run(conn, run_id) -> dict | None:
    run = conn.execute("SELECT * FROM runs WHERE id = %s", (run_id,)).fetchone()
    if run is None:
        return None
    rows = conn.execute(
        """SELECT a.answer_id, a.seq, a.status, a.error_type, a.error_message, a.claim_count, a.turns,
                  a.latency_ms, a.trace_ref,
                  c.claim_id, c.start_char, c.end_char, c.quote, c.label, c.fact_ids, c.reason,
                  c.matched_gold_id, c.gold_label, c.label_correct
           FROM answer_results a
           LEFT JOIN claim_results c ON c.run_id = a.run_id AND c.answer_id = a.answer_id
           WHERE a.run_id = %s
           ORDER BY a.seq, a.answer_id, c.start_char NULLS FIRST, c.end_char""",
        (run_id,),
    ).fetchall()
    answers: dict[str, dict] = {}
    for r in rows:
        a = answers.get(r["answer_id"])
        if a is None:
            a = answers[r["answer_id"]] = {
                k: r[k] for k in ("answer_id", "status", "error_type", "error_message", "claim_count",
                                  "turns", "latency_ms", "trace_ref")}
            a["claims"] = []
        if r["claim_id"] is not None:
            a["claims"].append({k: r[k] for k in ("claim_id", "start_char", "end_char", "quote", "label",
                                                  "fact_ids", "reason", "matched_gold_id", "gold_label",
                                                  "label_correct")})
    run = dict(run)
    run["id"] = str(run["id"])
    for k in ("created_at", "finished_at"):
        run[k] = run[k].isoformat() if run[k] else None
    run["answers"] = list(answers.values())
    return run
