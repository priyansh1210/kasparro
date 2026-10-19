"""Deterministic harness: exact (answer_id, start_char, end_char) span matching after a
quote-equality check, extraction and joint precision/recall/F1, and full accounting of
missed, extra and wrong-label claims and answer errors."""
from __future__ import annotations

from dataclasses import dataclass

from .data import GoldClaim


class ScoringError(Exception):
    pass


@dataclass
class AnswerOutcome:
    answer_id: str
    status: str  # ok | error
    claims: list[dict]
    error_type: str | None = None


def _ratio(num: int, den: int) -> float:
    return round(num / den, 6) if den else 0.0


def _f1(num: int, p: int, g: int) -> float:
    return round(2 * num / (p + g), 6) if (p + g) else 0.0


def check_outcomes(scheduled_ids: list[str], outcomes: list[AnswerOutcome]) -> None:
    ids = [o.answer_id for o in outcomes]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise ScoringError(f"duplicated answer outcomes: {dupes}")
    missing = sorted(set(scheduled_ids) - set(ids))
    if missing:
        raise ScoringError(f"missing answer outcomes: {missing}")
    unexpected = sorted(set(ids) - set(scheduled_ids))
    if unexpected:
        raise ScoringError(f"outcomes for unscheduled answers: {unexpected}")


def score(scheduled_ids: list[str], outcomes: list[AnswerOutcome], answers_text: dict[str, str],
          gold: list[GoldClaim] | None) -> dict:
    """Score a run. gold=None means an unlabeled (check) split: quality fields stay null."""
    check_outcomes(scheduled_ids, outcomes)
    errors = [o for o in outcomes if o.status != "ok"]
    error_counts: dict[str, int] = {}
    for o in errors:
        error_counts[o.error_type or "error"] = error_counts.get(o.error_type or "error", 0) + 1
    preds = [(o.answer_id, c) for o in outcomes if o.status == "ok" for c in o.claims]
    for aid, c in preds:
        if answers_text[aid][c["start_char"]:c["end_char"]] != c["quote"]:
            raise ScoringError(f"prediction {c['claim_id']} quote does not equal its span")
    base = {
        "answers_scheduled": len(scheduled_ids),
        "answers_ok": len(outcomes) - len(errors),
        "answers_error": len(errors),
        "answers_empty": sum(1 for o in outcomes if o.status == "ok" and not o.claims),
        "error_counts": error_counts,
        "P": len(preds),
    }
    if gold is None:
        base.update({"G": None, "M": None, "C": None, "metrics": None, "missed_gold_ids": None,
                     "unmatched_prediction_ids": [c["claim_id"] for _, c in preds],
                     "wrong_label_ids": None, "matches": None})
        return base

    scheduled = set(scheduled_ids)
    gold = [g for g in gold if g.answer_id in scheduled]
    gold_by_span = {(g.answer_id, g.start_char, g.end_char): g for g in gold}
    used: set[str] = set()
    matches: dict[str, dict] = {}  # prediction claim_id -> match info
    unmatched, wrong = [], []
    M = C = 0
    for aid, c in preds:
        g = gold_by_span.get((aid, c["start_char"], c["end_char"]))
        if g is None or g.claim_id in used or g.quote != c["quote"]:
            unmatched.append(c["claim_id"])
            continue
        used.add(g.claim_id)
        M += 1
        correct = g.expected_label == c["label"]
        C += correct
        if not correct:
            wrong.append(c["claim_id"])
        matches[c["claim_id"]] = {"gold_claim_id": g.claim_id, "gold_label": g.expected_label,
                                  "label_correct": correct}
    G, P = len(gold), len(preds)
    if G == 0 and not scheduled:
        metrics = None
    else:
        metrics = {
            "extraction": {"precision": _ratio(M, P), "recall": _ratio(M, G), "f1": _f1(M, P, G)},
            "joint": {"precision": _ratio(C, P), "recall": _ratio(C, G), "f1": _f1(C, P, G)},
            "coverage": _ratio(C, G),
        }
    base.update({
        "G": G, "M": M, "C": C, "metrics": metrics,
        "missed_gold_ids": [g.claim_id for g in gold if g.claim_id not in used],
        "unmatched_prediction_ids": unmatched,
        "wrong_label_ids": wrong,
        "matches": matches,
    })
    return base
