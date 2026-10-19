"""Claim extraction and classification agent.

Loop: at most MAX_MODEL_TURNS model requests per answer. Tool calls are executed by a
validating executor. The final JSON is parsed, quotes (v1) or sentence numbers (v2) are
mapped to offsets by Python, and everything is validated. Any failure is an answer-level
error with no accepted predictions."""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field

from .config import LABELS, MAX_MODEL_TURNS, PROMPTS_DIR
from .data import Answer, all_fact_ids
from .facts import ToolError, execute_tool_call, known_brands, tool_schema
from .providers import Provider, ProviderError, ProviderTimeout
from .segment import LocateError, locate_quotes, split_sentences

# Each agent version is a prompt file plus an output mode. v2 changes exactly one
# behaviour relative to v1; see README "The v2 change".
AGENT_VERSIONS = {
    "v1": {"prompt": "v1.md", "mode": "quote"},
    "v2": {"prompt": "v2.md", "mode": "quote"},
}


def prompt_text(version: str) -> str:
    return (PROMPTS_DIR / AGENT_VERSIONS[version]["prompt"]).read_text(encoding="utf-8")


def prompt_hash(version: str) -> str:
    return hashlib.sha256(prompt_text(version).encode("utf-8")).hexdigest()


class AnswerError(Exception):
    def __init__(self, error_type: str, message: str):
        super().__init__(message)
        self.error_type = error_type
        self.message = message


class OutputInvalid(Exception):
    """Model output failed validation; may be repaired if turns remain."""


@dataclass
class AgentResult:
    answer_id: str
    status: str  # "ok" | "error"
    claims: list[dict] = field(default_factory=list)
    error_type: str | None = None
    error_message: str | None = None
    turns: int = 0
    latency_ms: int = 0
    trace: list[dict] = field(default_factory=list)
    trace_ref: str | None = None

    def output(self) -> dict:
        return {"answer_id": self.answer_id, "claims": self.claims}


def build_user_message(answer: Answer, mode: str) -> str:
    payload = {
        "answer_id": answer.answer_id,
        "brand_id": answer.brand_id,
        "question": answer.question,
        "ai_answer": answer.ai_answer,
        "known_brand_ids": known_brands(),
    }
    if mode == "sentence":
        # Python segmentation of the whole answer (advice included); not a claim list.
        payload["sentences"] = [{"n": s.index, "text": s.text} for s in split_sentences(answer.ai_answer)]
    return json.dumps(payload, ensure_ascii=False, indent=1)


_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


def _parse_json(content: str | None) -> dict:
    if not content or not content.strip():
        raise OutputInvalid("final message was empty; expected a JSON object")
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = _JSON_BLOCK.search(text)
        if not m:
            raise OutputInvalid("final message is not JSON") from None
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError as exc:
            raise OutputInvalid(f"final message is not valid JSON: {exc.msg}") from None
    if not isinstance(data, dict):
        raise OutputInvalid("final JSON must be an object")
    return data


def _limit_reason(reason: str) -> str:
    sentences = split_sentences(reason.strip())
    if len(sentences) <= 2:
        return reason.strip()
    return reason.strip()[: sentences[1].end]


def validate_output(answer: Answer, data: dict, mode: str) -> list[dict]:
    """Turn the model JSON into validated claims (sorted, offsets computed by Python)."""
    if data.get("answer_id", answer.answer_id) != answer.answer_id:
        raise OutputInvalid("answer_id in output does not match the input")
    raw_claims = data.get("claims")
    if not isinstance(raw_claims, list):
        raise OutputInvalid("'claims' must be a list")
    text = answer.ai_answer
    known_ids = all_fact_ids()
    item_key = "quote" if mode == "quote" else "sentence"
    allowed_keys = {item_key, "label", "fact_ids", "reason"}

    items = []
    for i, c in enumerate(raw_claims):
        if not isinstance(c, dict):
            raise OutputInvalid(f"claim {i} is not an object")
        extra = set(c) - allowed_keys - {"quote", "sentence"}
        if extra:
            raise OutputInvalid(f"claim {i} has unexpected keys {sorted(extra)}")
        label = c.get("label")
        if label not in LABELS:
            raise OutputInvalid(f"claim {i} has unsupported label {str(label)[:30]!r}")
        fact_ids = c.get("fact_ids", [])
        if not isinstance(fact_ids, list) or not all(isinstance(f, str) for f in fact_ids):
            raise OutputInvalid(f"claim {i} fact_ids must be a list of strings")
        bad = [f for f in fact_ids if f not in known_ids]
        if bad:
            raise OutputInvalid(f"claim {i} cites unknown fact_ids {bad[:3]}")
        if len(set(fact_ids)) != len(fact_ids):
            raise OutputInvalid(f"claim {i} repeats a fact_id")
        reason = c.get("reason", "")
        if not isinstance(reason, str):
            raise OutputInvalid(f"claim {i} reason must be a string")
        items.append((c, label, fact_ids, _limit_reason(reason)))

    if mode == "quote":
        quotes = []
        for i, (c, *_rest) in enumerate(items):
            q = c.get("quote")
            if not isinstance(q, str):
                raise OutputInvalid(f"claim {i} quote must be a string")
            quotes.append(q)
        try:
            spans = locate_quotes(text, quotes)
        except LocateError as exc:
            raise OutputInvalid(str(exc)) from None
    else:
        sentences = split_sentences(text)
        spans = []
        for i, (c, *_rest) in enumerate(items):
            n = c.get("sentence")
            if not isinstance(n, int) or isinstance(n, bool) or not 0 <= n < len(sentences):
                raise OutputInvalid(f"claim {i} sentence number {n!r} is out of range")
            spans.append((sentences[n].start, sentences[n].end))

    claims = []
    for (c, label, fact_ids, reason), (s, e) in zip(items, spans):
        claims.append({
            "claim_id": f"{answer.answer_id}:{s}:{e}", "start_char": s, "end_char": e,
            "quote": text[s:e], "label": label, "fact_ids": fact_ids, "reason": reason,
        })
    claims.sort(key=lambda c: c["start_char"])
    check_claims(text, answer.answer_id, claims)
    return claims


def check_claims(text: str, answer_id: str, claims: list[dict]) -> None:
    """Structural checks shared by the agent and the API response layer."""
    seen = set()
    prev_end = -1
    for c in claims:
        s, e = c["start_char"], c["end_char"]
        if not (isinstance(s, int) and isinstance(e, int) and 0 <= s < e <= len(text)):
            raise OutputInvalid(f"span {s}:{e} is out of bounds")
        if text[s:e] != c["quote"]:
            raise OutputInvalid(f"quote does not equal ai_answer[{s}:{e}]")
        if c["quote"] != c["quote"].strip():
            raise OutputInvalid("quote has leading or trailing whitespace")
        if c["claim_id"] != f"{answer_id}:{s}:{e}":
            raise OutputInvalid("claim_id does not match its span")
        if c["claim_id"] in seen:
            raise OutputInvalid(f"duplicate claim {c['claim_id']}")
        seen.add(c["claim_id"])
        if s < prev_end:
            raise OutputInvalid(f"claim {c['claim_id']} overlaps the previous claim")
        prev_end = e


def run_agent(answer: Answer, version: str, provider: Provider) -> AgentResult:
    if version not in AGENT_VERSIONS:
        raise ValueError(f"unknown agent version {version}")
    mode = AGENT_VERSIONS[version]["mode"]
    messages: list[dict] = [
        {"role": "system", "content": prompt_text(version)},
        {"role": "user", "content": build_user_message(answer, mode)},
    ]
    tools = [tool_schema()]
    result = AgentResult(answer.answer_id, "error")
    started = time.perf_counter()
    try:
        for turn in range(1, MAX_MODEL_TURNS + 1):
            result.turns = turn
            t0 = time.perf_counter()
            reply = provider.complete(messages, tools)
            result.trace.append({"turn": turn, "request_messages": len(messages),
                                 "latency_ms": int((time.perf_counter() - t0) * 1000),
                                 "assistant": reply.message, "usage": reply.usage})
            messages.append(reply.message)
            if reply.tool_calls:
                for call in reply.tool_calls:
                    tool_result = execute_tool_call(call.name, call.arguments)
                    result.trace.append({"turn": turn, "tool_call": {"name": call.name, "arguments": call.arguments},
                                         "tool_result_rows": len(tool_result["facts"])})
                    messages.append({"role": "tool", "tool_call_id": call.id,
                                     "content": json.dumps(tool_result, ensure_ascii=False)})
                continue
            try:
                claims = validate_output(answer, _parse_json(reply.content), mode)
            except OutputInvalid as exc:
                result.trace.append({"turn": turn, "validation_error": str(exc)})
                if turn == MAX_MODEL_TURNS:
                    raise AnswerError("invalid_output", str(exc)) from None
                messages.append({"role": "user", "content":
                                 f"Your output failed validation: {exc}. Return the complete corrected "
                                 "JSON object only, following the same output format."})
                continue
            result.status, result.claims = "ok", claims
            return result
        raise AnswerError("turn_limit_exhausted", f"no valid final output within {MAX_MODEL_TURNS} model turns")
    except AnswerError as exc:
        result.error_type, result.error_message = exc.error_type, exc.message
    except ToolError as exc:
        result.error_type, result.error_message = exc.error_type, str(exc)
    except ProviderTimeout as exc:
        result.error_type, result.error_message = exc.error_type, str(exc)
    except ProviderError as exc:
        result.error_type, result.error_message = exc.error_type, str(exc)
    finally:
        result.latency_ms = int((time.perf_counter() - started) * 1000)
    result.claims = []
    return result
