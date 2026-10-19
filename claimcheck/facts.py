"""The single read-only tool exposed to the model, plus its validating executor."""
from __future__ import annotations

import json

from .config import FACT_VERSION
from .data import facts_by_brand

TOOL_NAME = "get_brand_facts"


class ToolError(Exception):
    """Illegal tool name, bad arguments or unknown brand. Always an answer-level error."""

    def __init__(self, error_type: str, message: str):
        super().__init__(message)
        self.error_type = error_type


def known_brands() -> list[str]:
    return sorted(facts_by_brand())


def tool_schema() -> dict:
    return {
        "type": "function",
        "function": {
            "name": TOOL_NAME,
            "description": "Read-only lookup of the official catalogue fact rows for one brand. "
                           "Returns every fact row for that brand (all its models).",
            "parameters": {
                "type": "object",
                "properties": {
                    "brand_id": {"type": "string", "enum": known_brands(),
                                 "description": "Catalogue brand identifier."}
                },
                "required": ["brand_id"],
            },
        },
    }


def get_brand_facts(brand_id: str) -> dict:
    brands = facts_by_brand()
    if brand_id not in brands:
        raise ToolError("unknown_brand", f"unknown brand_id {brand_id!r}")
    return {
        "brand_id": brand_id,
        "fact_version": FACT_VERSION,
        "facts": [f.to_tool_row() for f in brands[brand_id]],
    }


def execute_tool_call(name: str, raw_arguments: str | None) -> dict:
    """Validate the tool name and arguments, then run the lookup."""
    if name != TOOL_NAME:
        raise ToolError("illegal_tool", f"model requested an unknown tool {name[:60]!r}")
    try:
        args = json.loads(raw_arguments or "{}")
    except json.JSONDecodeError as exc:
        raise ToolError("invalid_tool_arguments", f"tool arguments are not JSON: {exc.msg}") from None
    if not isinstance(args, dict) or set(args) != {"brand_id"} or not isinstance(args["brand_id"], str):
        raise ToolError("invalid_tool_arguments", "tool arguments must be exactly {brand_id: string}")
    return get_brand_facts(args["brand_id"])
