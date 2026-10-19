"""CSV loading. Files are read with the csv module, UTF-8 and newline='' so quoted
commas and embedded newlines stay inside fields and ai_answer is never altered."""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path

from .config import DATA_DIR

ANSWER_FIELDS = ["answer_id", "split", "brand_id", "question", "ai_answer"]
FACT_FIELDS = ["fact_id", "brand_id", "model_id", "field", "value", "value_type",
               "unit", "condition", "valid_from", "valid_to"]
GOLD_FIELDS = ["answer_id", "claim_id", "start_char", "end_char", "quote", "expected_label",
               "evidence_fact_ids", "explanation", "difficulty_tags"]


@dataclass(frozen=True)
class Answer:
    answer_id: str
    split: str
    brand_id: str
    question: str
    ai_answer: str


@dataclass(frozen=True)
class Fact:
    fact_id: str
    brand_id: str
    model_id: str
    field: str
    value: object  # typed: float/int, bool or str
    value_type: str
    unit: str | None
    condition: str | None
    valid_from: date
    valid_to: date

    def to_tool_row(self) -> dict:
        return {
            "fact_id": self.fact_id, "model_id": self.model_id, "field": self.field,
            "value": self.value, "value_type": self.value_type, "unit": self.unit,
            "condition": self.condition, "valid_from": self.valid_from.isoformat(),
            "valid_to": self.valid_to.isoformat(),
        }


@dataclass(frozen=True)
class GoldClaim:
    answer_id: str
    claim_id: str
    start_char: int
    end_char: int
    quote: str
    expected_label: str


def read_csv(path: Path, expected_fields: list[str]) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != expected_fields:
            raise ValueError(f"{path.name}: unexpected header {reader.fieldnames}")
        return list(reader)


def parse_value(raw: str, value_type: str) -> object:
    if value_type == "number":
        num = float(raw)
        return int(num) if num.is_integer() else num
    if value_type == "boolean":
        lowered = raw.strip().lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        raise ValueError(f"invalid boolean text {raw!r}")
    if value_type == "string":
        return raw
    raise ValueError(f"unknown value_type {value_type!r}")


def load_answers(path: Path | None = None) -> list[Answer]:
    rows = read_csv(path or DATA_DIR / "answers.csv", ANSWER_FIELDS)
    return [Answer(**r) for r in rows]


def load_facts(path: Path | None = None) -> list[Fact]:
    rows = read_csv(path or DATA_DIR / "brand_facts.csv", FACT_FIELDS)
    facts = []
    for r in rows:
        facts.append(Fact(
            fact_id=r["fact_id"], brand_id=r["brand_id"], model_id=r["model_id"],
            field=r["field"], value=parse_value(r["value"], r["value_type"]),
            value_type=r["value_type"], unit=r["unit"] or None, condition=r["condition"] or None,
            valid_from=date.fromisoformat(r["valid_from"]), valid_to=date.fromisoformat(r["valid_to"]),
        ))
    return facts


def load_gold(path: Path | None = None) -> list[GoldClaim]:
    rows = read_csv(path or DATA_DIR / "development_gold.csv", GOLD_FIELDS)
    return [GoldClaim(r["answer_id"], r["claim_id"], int(r["start_char"]), int(r["end_char"]),
                      r["quote"], r["expected_label"]) for r in rows]


@lru_cache(maxsize=1)
def facts_by_brand() -> dict[str, list[Fact]]:
    out: dict[str, list[Fact]] = {}
    for f in load_facts():
        out.setdefault(f.brand_id, []).append(f)
    return out


@lru_cache(maxsize=1)
def all_fact_ids() -> frozenset[str]:
    return frozenset(f.fact_id for f in load_facts())


def file_hashes() -> dict[str, str]:
    return {name: hashlib.sha256((DATA_DIR / name).read_bytes()).hexdigest()
            for name in ("answers.csv", "brand_facts.csv", "development_gold.csv")}
