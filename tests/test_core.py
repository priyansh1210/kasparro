import csv
import io
import json

import pytest

from claimcheck.agent import OutputInvalid, check_claims, run_agent, validate_output
from claimcheck.data import Answer, load_answers, load_facts, load_gold, parse_value, read_csv
from claimcheck.facts import ToolError, execute_tool_call, get_brand_facts
from claimcheck.providers import FakeProvider, ProviderTimeout, final_turn, tool_turn
from claimcheck.scoring import AnswerOutcome, ScoringError, score
from claimcheck.segment import locate_quotes, split_sentences

ANSWERS = {a.answer_id: a for a in load_answers()}
GOLD = load_gold()


# ---------- CSV parsing ----------

def test_csv_quoted_commas_and_newlines(tmp_path):
    p = tmp_path / "a.csv"
    p.write_bytes(b'answer_id,split,brand_id,question,ai_answer\r\n'
                  b'X1,development,cleartrail,"Q, with comma","Line one, still one.\n\nPara two."\r\n')
    rows = read_csv(p, ["answer_id", "split", "brand_id", "question", "ai_answer"])
    assert len(rows) == 1
    assert rows[0]["question"] == "Q, with comma"
    assert rows[0]["ai_answer"] == "Line one, still one.\n\nPara two."


def test_answers_loaded_exactly():
    assert len(ANSWERS) == 50
    assert sum(a.split == "development" for a in ANSWERS.values()) == 40
    raw = (load_answers.__globals__["DATA_DIR"] / "answers.csv").read_bytes().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(raw, newline="")))
    for r in rows:
        assert ANSWERS[r["answer_id"]].ai_answer == r["ai_answer"]
    assert "\n\n" in ANSWERS["A01"].ai_answer and "\r" not in ANSWERS["A01"].ai_answer


def test_all_gold_quotes_equal_spans():
    assert len(GOLD) == 376
    for g in GOLD:
        assert ANSWERS[g.answer_id].ai_answer[g.start_char:g.end_char] == g.quote


def test_typed_values_never_bool_of_string():
    assert parse_value("false", "boolean") is False
    assert parse_value("true", "boolean") is True
    assert parse_value("1299", "number") == 1299
    assert parse_value("5.3", "string") == "5.3"
    with pytest.raises(ValueError):
        parse_value("yes", "boolean")
    assert len(load_facts()) == 132


def test_segmenter_aligns_with_every_gold_span_and_keeps_decimals():
    for aid in {g.answer_id for g in GOLD}:
        spans = {(s.start, s.end) for s in split_sentences(ANSWERS[aid].ai_answer)}
        for g in GOLD:
            if g.answer_id == aid:
                assert (g.start_char, g.end_char) in spans, g.claim_id
    assert [s.text for s in split_sentences("It weighs 0.35 kg. Warranty is 1.5 years.")] == [
        "It weighs 0.35 kg.", "Warranty is 1.5 years."]


# ---------- offsets / validation ----------

A = Answer("T1", "development", "cleartrail", "q?",
           "Advice first. ClearTrail Mini costs INR 1,299. ClearTrail Mini costs INR 1,299. Last one.")


def claim(q, label="unknown", fact_ids=None, reason="r."):
    return {"quote": q, "label": label, "fact_ids": fact_ids or [], "reason": reason}


def test_valid_offsets_and_repeated_quote_resolution():
    q = "ClearTrail Mini costs INR 1,299."
    out = validate_output(A, {"claims": [claim(q), claim(q, "supported", ["cleartrail.mini.price_2026"])]}, "quote")
    assert [(c["start_char"], c["end_char"]) for c in out] == [(14, 46), (47, 79)]
    for c in out:
        assert A.ai_answer[c["start_char"]:c["end_char"]] == c["quote"]
        assert c["claim_id"] == f"T1:{c['start_char']}:{c['end_char']}"


def test_quote_not_in_text_or_padded_is_invalid():
    with pytest.raises(OutputInvalid):
        validate_output(A, {"claims": [claim("ClearTrail Mini costs INR 1299.")]}, "quote")
    with pytest.raises(OutputInvalid):
        validate_output(A, {"claims": [claim(" Last one.")]}, "quote")


def test_third_copy_of_quote_would_overlap_is_invalid():
    q = "ClearTrail Mini costs INR 1,299."
    with pytest.raises(OutputInvalid):
        validate_output(A, {"claims": [claim(q), claim(q), claim(q)]}, "quote")


def test_check_claims_rejects_bad_offsets_duplicates_overlaps():
    t = A.ai_answer
    good = {"claim_id": "T1:0:13", "start_char": 0, "end_char": 13, "quote": t[0:13]}
    check_claims(t, "T1", [good])
    with pytest.raises(OutputInvalid):
        check_claims(t, "T1", [{**good, "end_char": 999, "claim_id": "T1:0:999"}])
    with pytest.raises(OutputInvalid):
        check_claims(t, "T1", [{**good, "quote": "Advice first!"}])
    with pytest.raises(OutputInvalid):
        check_claims(t, "T1", [good, good])
    overlap = {"claim_id": "T1:5:20", "start_char": 5, "end_char": 20, "quote": t[5:20]}
    with pytest.raises(OutputInvalid):
        check_claims(t, "T1", [good, overlap])


def test_sentence_mode_maps_numbers_and_rejects_out_of_range():
    out = validate_output(A, {"claims": [{"sentence": 1, "label": "supported",
                                          "fact_ids": ["cleartrail.mini.price_2026"], "reason": "ok."}]}, "sentence")
    assert out[0]["quote"] == "ClearTrail Mini costs INR 1,299."
    with pytest.raises(OutputInvalid):
        validate_output(A, {"claims": [{"sentence": 9, "label": "unknown", "fact_ids": [], "reason": ""}]}, "sentence")


def test_reason_limited_to_two_sentences():
    out = validate_output(A, {"claims": [claim("Last one.", reason="One. Two. Three.")]}, "quote")
    assert out[0]["reason"] == "One. Two."


# ---------- tool executor ----------

def test_tool_executor_validates_name_and_brand():
    res = execute_tool_call("get_brand_facts", json.dumps({"brand_id": "stonewave"}))
    assert res["fact_version"] == "speaker-catalogue-v4" and len(res["facts"]) == 44
    assert all(f["fact_id"].startswith("stonewave.") for f in res["facts"])
    with pytest.raises(ToolError) as e:
        execute_tool_call("delete_everything", "{}")
    assert e.value.error_type == "illegal_tool"
    with pytest.raises(ToolError) as e:
        get_brand_facts("rivalsound")
    assert e.value.error_type == "unknown_brand"
    with pytest.raises(ToolError):
        execute_tool_call("get_brand_facts", '{"brand_id": "cleartrail", "x": 1}')


# ---------- agent with fake provider ----------

A01 = ANSWERS["A01"]
Q1 = "For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping."


def _run(script, version="v1", answer=A01):
    fp = FakeProvider(script)
    return run_agent(answer, version, fp), fp


def test_agent_success_path():
    res, fp = _run([tool_turn("cleartrail"),
                    final_turn({"answer_id": "A01", "claims": [claim(Q1, "supported", ["cleartrail.mini.price_2026"])]})])
    assert res.status == "ok" and res.turns == 2
    assert res.claims[0]["claim_id"] == "A01:1620:1767"
    tool_msgs = [m for m in fp.payloads[1]["messages"] if m["role"] == "tool"]
    assert json.loads(tool_msgs[0]["content"])["brand_id"] == "cleartrail"


def test_valid_empty_output_is_ok():
    res, _ = _run([tool_turn("cleartrail"), final_turn({"answer_id": "A01", "claims": []})])
    assert res.status == "ok" and res.claims == []


def test_malformed_output_then_exhaustion_is_error():
    res, _ = _run([tool_turn("cleartrail"), final_turn("not json"), final_turn("{still bad")])
    assert res.status == "error" and res.error_type == "invalid_output" and res.claims == []


def test_repair_turn_can_fix_output():
    res, fp = _run([tool_turn("cleartrail"), final_turn("oops"), final_turn({"claims": [claim(Q1)]})])
    assert res.status == "ok" and res.turns == 3
    assert "failed validation" in fp.payloads[2]["messages"][-1]["content"]


@pytest.mark.parametrize("bad", [
    {"claims": [claim(Q1, "true")]},                                    # unsupported label
    {"claims": [claim(Q1, "supported", ["cleartrail.mini.colour"])]},   # invented fact id
])
def test_bad_labels_and_fact_ids_are_errors(bad):
    res, _ = _run([tool_turn("cleartrail"), final_turn(bad), final_turn(bad)])
    assert res.status == "error" and res.error_type == "invalid_output" and res.claims == []


def test_illegal_tool_is_error():
    res, _ = _run([tool_turn("cleartrail", name="run_shell")])
    assert res.status == "error" and res.error_type == "illegal_tool"


def test_unknown_brand_tool_request_is_error():
    res, _ = _run([tool_turn("rivalsound")])
    assert res.status == "error" and res.error_type == "unknown_brand"


def test_timeout_is_error_not_unknown():
    res, _ = _run([ProviderTimeout("provider request exceeded 120s timeout")])
    assert res.status == "error" and res.error_type == "provider_timeout" and res.claims == []


def test_turn_exhaustion():
    res, _ = _run([tool_turn("cleartrail"), tool_turn("cleartrail"), tool_turn("cleartrail")])
    assert res.status == "error" and res.error_type == "turn_limit_exhausted" and res.turns == 3


@pytest.mark.parametrize("version", ["v1", "v2"])
def test_gold_never_enters_model_or_tool_payloads(version):
    res, fp = _run([tool_turn("cleartrail"), final_turn({"claims": []})], version=version)
    blob = json.dumps(fp.payloads)
    for g in GOLD:
        if g.answer_id == "A01":
            assert g.claim_id not in blob
            assert f"{g.start_char}:{g.end_char}" not in blob
    explanations = [r["explanation"] for r in csv.DictReader(
        open(load_answers.__globals__["DATA_DIR"] / "development_gold.csv", encoding="utf-8", newline=""))]
    assert not any(e in blob for e in explanations)
    assert "expected_label" not in blob and "difficulty_tags" not in blob


# ---------- scorer ----------

def _mk(aid, s, e, label, text):
    return {"claim_id": f"{aid}:{s}:{e}", "start_char": s, "end_char": e, "quote": text[s:e], "label": label}


def _gold_for(aid):
    return [g for g in GOLD if g.answer_id == aid]


def test_perfect_output():
    g = _gold_for("A01")
    preds = [_mk("A01", x.start_char, x.end_char, x.expected_label, A01.ai_answer) for x in g]
    s = score(["A01"], [AnswerOutcome("A01", "ok", preds)], {"A01": A01.ai_answer}, GOLD)
    assert s["metrics"]["joint"] == {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    assert s["missed_gold_ids"] == [] and s["unmatched_prediction_ids"] == []


def test_missed_claims_extra_advice_and_wrong_label():
    g = _gold_for("A01")
    preds = [_mk("A01", x.start_char, x.end_char, x.expected_label, A01.ai_answer) for x in g[2:]]
    adv = split_sentences(A01.ai_answer)[0]
    preds.append(_mk("A01", adv.start, adv.end, "unknown", A01.ai_answer))  # advice extracted
    wrong = "unknown" if preds[0]["label"] != "unknown" else "supported"
    preds[0] = {**preds[0], "label": wrong}
    preds.sort(key=lambda c: c["start_char"])
    s = score(["A01"], [AnswerOutcome("A01", "ok", preds)], {"A01": A01.ai_answer}, GOLD)
    G = len(g)
    assert (s["G"], s["P"], s["M"], s["C"]) == (G, G - 1, G - 2, G - 3)
    assert s["missed_gold_ids"] == [g[0].claim_id, g[1].claim_id]
    assert s["unmatched_prediction_ids"] == [f"A01:{adv.start}:{adv.end}"]
    assert len(s["wrong_label_ids"]) == 1
    assert s["metrics"]["extraction"]["f1"] == round(2 * (G - 2) / (2 * G - 1), 6)


def test_provider_error_answer_keeps_gold_in_G_and_empty_valid():
    s = score(["A01", "A02"], [AnswerOutcome("A01", "error", [], "provider_error"), AnswerOutcome("A02", "ok", [])],
              {"A01": A01.ai_answer, "A02": ANSWERS["A02"].ai_answer}, GOLD)
    assert s["G"] == len(_gold_for("A01")) + len(_gold_for("A02"))
    assert s["P"] == 0 and s["M"] == 0
    assert s["metrics"]["joint"]["f1"] == 0.0 and s["metrics"]["extraction"]["precision"] == 0.0
    assert s["answers_error"] == 1 and s["answers_empty"] == 1 and s["error_counts"] == {"provider_error": 1}


def test_worked_example_G10_P10_M8_C7():
    from claimcheck.data import GoldClaim
    text = " ".join(f"S{i}." for i in range(20))
    sents = split_sentences(text)
    gold = [GoldClaim("Z", f"Z:{s.start}:{s.end}", s.start, s.end, s.text, "supported") for s in sents[:10]]
    preds = [_mk("Z", s.start, s.end, "supported", text) for s in sents[:7]]
    preds.append(_mk("Z", sents[7].start, sents[7].end, "unknown", text))
    preds += [_mk("Z", s.start, s.end, "supported", text) for s in sents[10:12]]
    s = score(["Z"], [AnswerOutcome("Z", "ok", preds)], {"Z": text}, gold)
    assert (s["G"], s["P"], s["M"], s["C"]) == (10, 10, 8, 7)
    assert s["metrics"]["extraction"] == {"precision": 0.8, "recall": 0.8, "f1": 0.8}
    assert s["metrics"]["joint"] == {"precision": 0.7, "recall": 0.7, "f1": 0.7}


def test_rejects_missing_or_duplicated_outcomes():
    texts = {"A01": A01.ai_answer, "A02": ANSWERS["A02"].ai_answer}
    with pytest.raises(ScoringError):
        score(["A01", "A02"], [AnswerOutcome("A01", "ok", [])], texts, GOLD)
    with pytest.raises(ScoringError):
        score(["A01"], [AnswerOutcome("A01", "ok", []), AnswerOutcome("A01", "ok", [])], texts, GOLD)


def test_check_split_metrics_are_null():
    s = score(["A41"], [AnswerOutcome("A41", "ok", [])], {"A41": ANSWERS["A41"].ai_answer}, None)
    assert s["metrics"] is None and s["G"] is None and s["M"] is None and s["C"] is None


def test_empty_split_null_metrics():
    assert score([], [], {}, GOLD)["metrics"] is None


def test_quote_must_equal_span_before_matching():
    g = _gold_for("A01")[0]
    bad = {"claim_id": g.claim_id, "start_char": g.start_char, "end_char": g.end_char, "quote": "x", "label": "unknown"}
    with pytest.raises(ScoringError):
        score(["A01"], [AnswerOutcome("A01", "ok", [bad])], {"A01": A01.ai_answer}, GOLD)
