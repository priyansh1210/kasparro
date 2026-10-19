"""Command line: python -m claimcheck.cli {init-db,run,classify} ..."""
from __future__ import annotations

import argparse
import json

from . import db
from .agent import run_agent
from .config import get_settings
from .data import load_answers
from .providers import build_provider
from .runner import evaluate


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="claimcheck")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init-db")
    r = sub.add_parser("run")
    r.add_argument("--version", choices=["v1", "v2"], required=True)
    r.add_argument("--split", choices=["development", "check"], required=True)
    r.add_argument("--workers", type=int, default=1)
    r.add_argument("--answers", nargs="*", help="optional subset (smoke runs only)")
    c = sub.add_parser("classify")
    c.add_argument("--version", choices=["v1", "v2"], required=True)
    c.add_argument("answer_id")
    args = p.parse_args(argv)

    if args.cmd == "init-db":
        db.init_schema()
        print("schema ready")
    elif args.cmd == "run":
        report = evaluate(args.version, args.split, answer_ids=args.answers, workers=args.workers)
        print(json.dumps({"run_id": report["run_id"], "report_dir": report.get("report_dir"),
                          "summary": {k: v for k, v in report["summary"].items()
                                      if k not in ("missed_gold_ids", "unmatched_prediction_ids",
                                                   "wrong_label_ids")}}, indent=1))
    elif args.cmd == "classify":
        answer = next(a for a in load_answers() if a.answer_id == args.answer_id)
        res = run_agent(answer, args.version, build_provider(get_settings()))
        print(json.dumps({"status": res.status, "error": res.error_type, "message": res.error_message,
                          "turns": res.turns, **res.output()}, indent=1))


if __name__ == "__main__":
    main()
