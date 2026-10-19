"""Thin FastAPI layer over the agent, runner and database."""
from __future__ import annotations

import uuid
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from . import db
from .agent import run_agent
from .config import get_settings
from .data import Answer
from .facts import known_brands
from .providers import Provider, ProviderError, build_provider
from .runner import evaluate

app = FastAPI(title="claimcheck")

# Tests override this to inject a fake provider.
provider_factory = lambda: build_provider(get_settings())  # noqa: E731


def _error(status: int, type_: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"type": type_, "message": message}})


@app.exception_handler(RequestValidationError)
async def _validation_handler(request: Request, exc: RequestValidationError):
    fields = sorted({".".join(str(p) for p in e["loc"][1:]) or "body" for e in exc.errors()})
    return _error(422, "invalid_request", f"invalid or forbidden fields: {', '.join(fields)[:300]}")


class ClassifyRequest(BaseModel):
    # extra='forbid': any gold / claim-list field (claims, labels, spans...) is rejected with 422
    model_config = ConfigDict(extra="forbid")
    answer_id: str = Field(min_length=1, max_length=64)
    brand_id: str = Field(min_length=1, max_length=64)
    question: str = Field(max_length=5000)
    ai_answer: str = Field(min_length=1, max_length=50000)
    agent_version: Literal["v1", "v2"]


class EvaluationRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    agent_version: Literal["v1", "v2"]
    split: Literal["development", "check"]


@app.post("/classify")
def classify(req: ClassifyRequest):
    if req.brand_id not in known_brands():
        return _error(404, "unknown_brand", f"unknown primary brand_id {req.brand_id!r}")
    try:
        provider: Provider = provider_factory()
    except ProviderError as exc:
        return _error(502, exc.error_type, str(exc))
    answer = Answer(req.answer_id, "adhoc", req.brand_id, req.question, req.ai_answer)
    result = run_agent(answer, req.agent_version, provider)
    if result.status == "ok":
        return result.output()
    status = 504 if result.error_type == "provider_timeout" else 502
    return _error(status, result.error_type or "agent_error", result.error_message or "agent failed")


@app.post("/evaluation-runs", status_code=201)
def create_evaluation_run(req: EvaluationRunRequest):
    try:
        provider: Provider = provider_factory()
    except ProviderError as exc:
        return _error(502, exc.error_type, str(exc))
    report = evaluate(req.agent_version, req.split, provider, log=lambda *_: None)
    s = report["summary"]
    return {"run_id": report["run_id"], "status": report["status"],
            "counts": {k: s[k] for k in ("answers_scheduled", "answers_ok", "answers_error",
                                         "answers_empty", "error_counts", "G", "P", "M", "C")},
            "metrics": s["metrics"]}


@app.get("/evaluation-runs/{run_id}")
def get_evaluation_run(run_id: uuid.UUID):
    with db.connect() as conn:
        run = db.get_run(conn, run_id)
    if run is None:
        return _error(404, "run_not_found", f"run {run_id} not found")
    return run
