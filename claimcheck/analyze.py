"""Error breakdown for a development report: python -m claimcheck.analyze runs/<dir>/report.json"""
from __future__ import annotations

import json
import sys
from collections import Counter

from .data import load_answers, load_gold
from .segment import split_sentences


def main(path: str) -> None:
    report = json.loads(open(path, encoding="utf-8").read())
    s = report["summary"]
    answers = {a.answer_id: a.ai_answer for a in load_answers()}
    gold = {g.claim_id: g for g in load_gold()}
    seg = {aid: {(x.start, x.end) for x in split_sentences(t)} for aid, t in answers.items()}
    preds = {c["claim_id"]: c for a in report["answers"] for c in a["claims"]}
    extra_kind = Counter()
    for pid in s["unmatched_prediction_ids"]:
        aid = pid.split(":")[0]
        c = preds[pid]
        extra_kind["whole non-gold sentence" if (c["start_char"], c["end_char"]) in seg[aid]
                   else "partial/merged span"] += 1
    confusion = Counter()
    for pid in s["wrong_label_ids"]:
        c = preds[pid]
        confusion[f"{c['match']['gold_label']} -> {c['label']}"] += 1
    missed_by_label = Counter(gold[g].expected_label for g in s["missed_gold_ids"])
    print(json.dumps({"metrics": s["metrics"], "G": s["G"], "P": s["P"], "M": s["M"], "C": s["C"],
                      "errors": s["error_counts"], "extra_by_kind": extra_kind,
                      "missed_by_gold_label": missed_by_label,
                      "wrong_label_confusion": confusion}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
