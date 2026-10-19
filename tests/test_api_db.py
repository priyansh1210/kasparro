"""API validation, PostgreSQL persistence and joined retrieval. Needs a real PostgreSQL
reachable via DATABASE_URL; skipped with a visible reason otherwise."""
import uuid

import pytest
from fastapi.testclient import TestClient

from claimcheck import api, db
from claimcheck.config import get_settings
from claimcheck.data import load_answers
from claimcheck.providers import FakeProvider, ProviderTimeout, final_turn, tool_turn
from claimcheck.runner import evaluate

ANSWERS = {a.answer_id: a for a in load_answers()}
Q1 = "For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping."


def _db_available():
    if not get_settings().database_url:
        return False
    try:
        db.init_schema()
        return True
    except Exception:
        return False


needs_db = pytest.mark.skipif(not _db_available(), reason="PostgreSQL not reachable via DATABASE_URL")


@pytest.fixture
def client():
    return TestClient(api.app)


def _body(**kw):
    a = ANSWERS["A01"]
    body = {"answer_id": a.answer_id, "brand_id": a.brand_id, "question": a.question,
            "ai_answer": a.ai_answer, "agent_version": "v1"}
    body.update(kw)
    return body


def _use(script):
    fp = FakeProvider(script)
    api.provider_factory = lambda: fp
    return fp


def test_classify_200(client):
    _use([tool_turn("cleartrail"), final_turn({"claims": [{"quote": Q1, "label": "supported",
                                                           "fact_ids": ["cleartrail.mini.price_2026"], "reason": "ok."}]})])
    r = client.post("/classify", json=_body())
    assert r.status_code == 200
    assert r.json()["claims"][0]["claim_id"] == "A01:1620:1767"


@pytest.mark.parametrize("extra", [{"claims": []}, {"expected_label": "supported"}, {"start_char": 1},
                                   {"agent_version": "v3"}])
def test_classify_422_on_invalid_or_gold_fields(client, extra):
    r = client.post("/classify", json=_body(**extra))
    assert r.status_code == 422 and r.json()["error"]["type"] == "invalid_request"


def test_classify_422_missing_field(client):
    body = _body()
    del body["ai_answer"]
    assert client.post("/classify", json=body).status_code == 422


def test_classify_404_unknown_brand(client):
    r = client.post("/classify", json=_body(brand_id="rivalsound"))
    assert r.status_code == 404 and r.json()["error"]["type"] == "unknown_brand"


def test_classify_502_invalid_output(client):
    _use([tool_turn("cleartrail"), final_turn("bad"), final_turn("bad")])
    r = client.post("/classify", json=_body())
    assert r.status_code == 502 and r.json()["error"]["type"] == "invalid_output"


def test_classify_504_timeout(client):
    _use([ProviderTimeout("provider request exceeded 120s timeout")])
    r = client.post("/classify", json=_body())
    assert r.status_code == 504 and r.json()["error"]["type"] == "provider_timeout"


def test_run_requests_validated(client):
    assert client.post("/evaluation-runs", json={"agent_version": "v1", "split": "test"}).status_code == 422
    assert client.get("/evaluation-runs/not-a-uuid").status_code == 422


@needs_db
def test_get_missing_run_404(client):
    r = client.get(f"/evaluation-runs/{uuid.uuid4()}")
    assert r.status_code == 404


@needs_db
def test_persistence_and_joined_retrieval_ok_empty_error(client):
    # A01: success with one claim, A02: valid empty, A03: provider timeout
    fp = FakeProvider([tool_turn("cleartrail"),
                       final_turn({"claims": [{"quote": Q1, "label": "supported",
                                               "fact_ids": ["cleartrail.mini.price_2026"], "reason": "ok."}]}),
                       tool_turn("cloudnote"), final_turn({"claims": []}),
                       ProviderTimeout("provider request exceeded 120s timeout")])
    report = evaluate("v1", "development", fp, answer_ids=["A01", "A02", "A03"], write_files=False,
                      log=lambda *_: None)
    s = report["summary"]
    assert s["answers_ok"] == 2 and s["answers_error"] == 1 and s["answers_empty"] == 1
    assert s["P"] == 1 and s["M"] == 1 and s["C"] == 1

    r = client.get(f"/evaluation-runs/{report['run_id']}")
    assert r.status_code == 200
    run = r.json()
    assert run["status"] == "completed" and run["split"] == "development"
    assert run["file_hashes"]["answers.csv"].startswith("fa28e813")
    assert [a["answer_id"] for a in run["answers"]] == ["A01", "A02", "A03"]
    a01, a02, a03 = run["answers"]
    assert a01["claims"][0]["matched_gold_id"] == "A01:1620:1767" and a01["claims"][0]["label_correct"] is True
    assert a02["status"] == "ok" and a02["claims"] == []
    assert a03["status"] == "error" and a03["error_type"] == "provider_timeout" and a03["claims"] == []
    assert run["metrics"]["joint"]["precision"] == 1.0


@needs_db
def test_check_run_has_null_quality(client):
    fp = FakeProvider([tool_turn("stonewave"), final_turn({"claims": []})])
    api.provider_factory = lambda: fp
    aid = next(a.answer_id for a in ANSWERS.values() if a.split == "check")
    report = evaluate("v2", "check", fp, answer_ids=[aid], write_files=False, log=lambda *_: None)
    run = client.get(f"/evaluation-runs/{report['run_id']}").json()
    assert run["metrics"] is None and run["counts"]["G"] is None and run["counts"]["M"] is None


@needs_db
def test_unique_constraints_enforced():
    import psycopg
    fp = FakeProvider([tool_turn("cleartrail"), final_turn({"claims": []})])
    report = evaluate("v1", "development", fp, answer_ids=["A01"], write_files=False, log=lambda *_: None)
    with db.connect() as conn:
        with pytest.raises(psycopg.errors.UniqueViolation):
            conn.execute("INSERT INTO answer_results (run_id, answer_id, seq, status, claim_count, turns, latency_ms) "
                         "VALUES (%s, 'A01', 0, 'ok', 0, 1, 1)", (uuid.UUID(report["run_id"]),))
