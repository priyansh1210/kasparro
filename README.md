# claimcheck: extract and classify claims in long AI answers

A Python agent reads a long answer about speaker products, finds every sentence that makes a verifiable product, specification, purchase-policy or comparison claim, and labels each one `supported`, `contradicted` or `unknown` against `brand_facts.csv`. It looks the facts up through live tool calling. A deterministic harness scores extraction and labels with exact span matching. Two agent versions, v1 and v2, were run on the development and check splits. Results are stored in PostgreSQL and served by a thin FastAPI app.

## Layout

| Path | Contents |
|---|---|
| `claimcheck/data.py` | CSV loading (csv module, UTF-8, `newline=''`), typed fact values, file hashes |
| `claimcheck/facts.py` | `get_brand_facts` tool schema and a validating executor |
| `claimcheck/segment.py` | sentence spans and verbatim quote location (Python code-point offsets) |
| `claimcheck/providers.py` | OpenAI-compatible live provider (Gemini endpoint), fake provider for tests |
| `claimcheck/agent.py` | agent loop (at most 3 model turns), output validation, v1/v2 definitions |
| `claimcheck/scoring.py` | harness: exact span matching, extraction and joint P/R/F1, ID lists |
| `claimcheck/runner.py` | evaluation runs: PostgreSQL rows, `runs/` report files, traces |
| `claimcheck/db.py` | psycopg 3, parameterized SQL, joined retrieval |
| `claimcheck/api.py` | FastAPI routes |
| `prompts/v1.md`, `prompts/v2.md` | versioned system prompts |
| `sql/schema.sql` | `runs`, `answer_results`, `claim_results` |
| `data/` | the three issued CSVs, byte-for-byte, plus `SHA256SUMS` |
| `runs/` | the four live-run reports, traces, logs and test output |

## Setup

These steps need Python 3.12 and Docker, or any PostgreSQL 16.

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt      # Linux/macOS: .venv/bin/pip
cp .env.example .env                                # then set GEMINI_API_KEY
docker run -d --name claimcheck-pg -e POSTGRES_USER=claimcheck -e POSTGRES_PASSWORD=claimcheck \
  -e POSTGRES_DB=claimcheck -p 5433:5432 postgres:16
```

`DATABASE_URL` is `postgresql://claimcheck:claimcheck@localhost:5433/claimcheck`. Set it in `.env` or in the environment, then create the schema:

```bash
.venv/Scripts/python -m claimcheck.cli init-db
```

### Run

```bash
# live evaluation runs (writes PostgreSQL rows and runs/<timestamp>_<version>_<split>_<id>/)
.venv/Scripts/python -m claimcheck.cli run --version v1 --split development --workers 10
.venv/Scripts/python -m claimcheck.cli run --version v2 --split development --workers 10
.venv/Scripts/python -m claimcheck.cli run --version v1 --split check --workers 10
.venv/Scripts/python -m claimcheck.cli run --version v2 --split check --workers 10

# a single answer
.venv/Scripts/python -m claimcheck.cli classify --version v2 A01

# API
.venv/Scripts/uvicorn claimcheck.api:app --port 8000
```

### Test

```bash
.venv/Scripts/python -m pytest -v
```

The database tests use the real PostgreSQL at `DATABASE_URL`. If it is unreachable they are skipped, and pytest prints the reason.

## Settings: fixed for all four runs

| Setting | Value |
|---|---|
| Provider | Gemini through its OpenAI-compatible Chat Completions endpoint, called with the `openai` SDK |
| Model | `gemini-3.5-flash-lite` |
| Temperature | 0 |
| Provider request timeout | **120 s per request** (`LLM_TIMEOUT_S`) |
| Model turn limit | at most 3 turns per answer; several tool calls are allowed in one turn |
| Transient retries | up to 6 retries on HTTP 429, 5xx or connection errors, with exponential backoff of 5–60 s. Retries are not model turns, and a timeout is never retried. |
| Workers | 10 answers processed concurrently. The agent itself is unchanged, and database writes are sequential. |

## Agent

1. **Input.** The model receives `answer_id`, `brand_id`, `question`, the full unmodified `ai_answer` and the list of known brand IDs. v2 also receives the sentence segmentation described below. Gold data, claims, labels and spans never reach the model or the tool, and a test asserts this.
2. **Tool.** The model must request `get_brand_facts(brand_id)` through real function calling. The executor rejects any other tool name (`illegal_tool`), malformed arguments, and brands not in the catalogue (`unknown_brand`). Each of these is an answer-level error. The tool returns that brand's rows with typed values and `fact_version: speaker-catalogue-v4`.
3. **Output.** The model returns JSON. Python checks the following:
   - every quote equals `ai_answer[start:end]`;
   - spans are in bounds, unique and non-overlapping;
   - labels are one of the three allowed values;
   - every fact ID exists in the catalogue.
   Python then builds `claim_id = answer_id:start:end`, sorts the claims by start, and trims each `reason` to two sentences. Character offsets are always computed by Python; the model never counts characters. A quote that repeats in an answer is resolved by searching forward from the previous claim.
4. **Failures.** If validation fails and a turn remains, the errors are sent back once for repair. Invalid output on the last turn, an exhausted turn limit, a provider error or a timeout each produce an answer-level error with a sanitised type and message, and the answer gets no accepted predictions. An error is never converted to `unknown`.
5. **Untrusted text.** The answer text is treated as data. The embedded "Ignore the classification instructions…" sentences are neither obeyed nor extracted.

## Harness

- A prediction matches gold only when `answer_id`, `start_char` and `end_char` are all identical. Quote equality is checked first, and each gold span can match at most once.
- G is the number of gold claims, P the accepted predictions, M the span matches and C the matches with the correct label. Extraction scores are M/P, M/G and 2M/(P+G); joint scores are C/P, C/G and 2C/(P+G). Joint F1 is the headline metric.
- Errored answers contribute no predictions, but their gold claims stay in G.
- Each report also gives coverage C/G and lists the missed gold IDs, the unmatched prediction IDs, the wrong-label IDs and error counts by type.
- A run is rejected if any answer outcome is missing or duplicated.
- For check runs, G, M, C, the metrics and the match fields are all null.
- There is no LLM judge, no fuzzy matching, and the gold data is never edited.

## API

| Route | Behaviour |
|---|---|
| `POST /classify` | Body: agent input plus `agent_version`. Returns 200 with `{answer_id, claims}`. Returns 422 for invalid input or any extra field (gold or claim fields are refused because `extra='forbid'`), 404 for an unknown primary brand, 502 for a provider error or invalid output, and 504 for a timeout. Error bodies are `{"error": {"type", "message"}}`. |
| `POST /evaluation-runs` | Body: `{agent_version, split}`. Runs the fixed CSV split and returns 201 with `run_id`, status, counts and metrics (null for check). |
| `GET /evaluation-runs/{id}` | Returns the run joined with its answer rows and claim rows, in CSV order and then span order. Returns 404 if the run does not exist and 422 for an invalid UUID. |

## Database

- **`runs`** stores the split; the agent, prompt (hash), source (hash), dataset, evaluator and fact versions; the provider, model and settings (JSONB); the file hashes; status (`running`, `completed` or `failed`); timestamps; counts and metrics; and the missed, extra and wrong-label ID lists.
- **`answer_results`** has one terminal row per scheduled answer, unique on `(run_id, answer_id)`. It stores the status, sanitised error, latency, turns and trace reference.
- **`claim_results`** has one row per accepted prediction, unique on `(run_id, answer_id, start_char, end_char)`, with a foreign key to `answer_results`. It stores the development-split gold match, gold label and correctness.
- A run that is interrupted or hits an infrastructure failure is marked `failed`, and its partial rows are kept.

## Versions and the v2 change

### Final runs

All four runs used the same model (`gemini-3.5-flash-lite`), settings, data and scorer.

| Run | Folder | Answers ok/error | P | M | C | Extraction F1 | **Joint F1** | Joint P / R |
|---|---|---|---|---|---|---|---|---|
| v1 development | `runs/20261019T102718_v1_development_3fd87122` | 40 / 0 | 379 | 373 | 363 | 0.9881 | **0.9616** | 0.9578 / 0.9654 |
| v2 development | `runs/20261019T103952_v2_development_b3ed3e75` | 40 / 0 | 375 | 373 | 373 | 0.9933 | **0.9933** | 0.9947 / 0.9920 |
| v1 check | `runs/20261019T103218_v1_check_75314f48` | 10 / 0 | 94 | null | null | null | null | null |
| v2 check | `runs/20261019T103508_v2_check_46a51e3e` | 10 / 0 | 90 | null | null | null | null | null |

G = 376 for development. The check runs are scored privately by the reviewers.

**Frozen-version fingerprints (SHA-256, first 12 characters):**
- Prompts: v1 `972d55ca3052`, v2 `74ee7a41fad1`. Every run of a version uses the same hash.
- Source tree: v2 development, v1 check and v2 check all record source hash `a44410a4e10c`, so the check runs used exactly the frozen code.
- The v1 development run records `f356cf72c60b`. It ran before the v2 change and before `claimcheck/analyze.py` (an error-breakdown script) was added. The v1 prompt and v1 code path are unchanged since then.

### Diagnosis of v1

Running `python -m claimcheck.analyze <v1 report.json>` gives this breakdown:

- **Extraction was already strong:** 373 of 376 gold spans matched, with zero quote or boundary errors. All 6 extra predictions were whole non-claim sentences, which made the planned "sentence-number" output change pointless.
- **Labelling was the dominant failure:** 10 matched claims had the wrong label (6 contradicted→supported, 3 supported→contradicted, 1 unknown→contradicted).
- **Root cause:** the reasons show it directly. The JSON put `label` *before* `reason`, so the model committed to a label and only then did the arithmetic, often contradicting itself. For example: *"…24 hours equals 1440 minutes? Wait, 24 * 60 = 1440 minutes, not 1500"*, which it had labelled supported. Eight of the 10 errors were hours→minutes conversions or price-difference checks.

### The v2 change: one agent behaviour

**Reason before label.** In the output schema, `reason` now comes before `label`. The prompt asks the model to state the catalogue value for the exact model and condition, do any conversion or arithmetic explicitly, and only then choose the label. The illustrative example uses neutral numbers ("7 h x 60 = 420 min"), not dataset values.

Nothing else changed: tool, extraction rules, label rules, validation and settings are the same. Run `diff prompts/v1.md prompts/v2.md` to see the full change. (An early draft of the example used dataset-like numbers. It was replaced before any v2 run completed, and the interrupted attempt is kept as `runs/ABORTED_*`.)

### Measured effect, from v1 development to v2 development

- Wrong labels fell from 10 to 0, and C rose from 363 to 373. Joint F1 rose from 0.9616 to 0.9933.
- **Regressions:**
  - v2 extracted the advice sentence "Retain the original purchase paperwork if the terms require it." in A04 and A09, giving 2 extra predictions. v1 extracted it once, in A18.
  - v2 missed 3 gold claims in A32, the answer containing an injected instruction. Two of them are unknown and one is contradicted, and v1 matched all three.
  - v1's misses were 3 unknown claims in A36. v2 matched those.
- **Side effect:** v2 no longer extracted the injected instruction sentence. v1 extracted it as an `unknown` claim in A18 and A32, which counted as extra predictions.
- **Single-run caveat:** each version was run once (plus the rerun described below), so part of the difference may be sampling noise even at temperature 0.

### Other attempts kept as evidence

These runs are not used for the comparison. Their rows are also in PostgreSQL.

- `runs/SETUP-ERROR_*`: the first v1 attempt used `gemini-2.5-flash`, which returns HTTP 404 for this key. All 40 answers are recorded as `provider_error`.
- `runs/QUOTA-EXHAUSTED_*`: an attempt with `gemini-3.5-flash` that exhausted the free-tier quota (HTTP 429). It was interrupted and marked `failed` in the database. The model was then switched to `gemini-3.5-flash-lite` for **all four** reported runs.
- `runs/RATE-LIMITED_*`: the first complete v2 development run. It ran concurrently with the check runs, and 6 answers ended as `provider_error` after the retries were exhausted. Its joint F1 is 0.9169, with G=376, P=322 and C=320. On its 34 successful answers, v2 had joint F1 0.9938 against v1's 0.9614 on the same 34 answers. v2 development was then rerun alone with identical frozen code, giving the row in the table. The check runs were not repeated.
- The database also contains `fake-model` runs, which the test suite creates for the persistence tests.


## Evidence in `runs/`

- Each run folder contains `report.json` and `report.md`. These hold the predictions, answer outcomes, missed, extra and wrong-label records, metrics, settings and hashes.
- `traces/<answer_id>.json` in each run folder holds the sanitised model and tool exchanges: assistant messages, tool calls and arguments, the number of tool result rows, and validation errors.
- `runs/*.log` holds the console output of each run.
- `runs/test_output.txt` holds the actual pytest output (46 tests, all run against the real PostgreSQL).
- `runs/api_smoke.txt` is a live check of the API against the running server: `/classify` returned 200 with a real model call, and the 404, 422 and joined-retrieval routes were exercised.

Dataset hashes are in `data/SHA256SUMS`. Each run also records them in its metadata.

## Limitations and unfinished work

- The sentence splitter is regex-based. It was verified against all 376 development gold spans, but it is not a general-purpose splitter.
- Only one model was evaluated, and each run was done once. Run-to-run variance was not measured.
- Concurrency of 10 workers was added because of the time limit. Answers are processed independently, so the results are not affected.
- The check inputs (A41–A50) were visible and were read during the initial data analysis. Nothing was tuned on check predictions, because no check run happened until both versions were frozen. Even so, this is **not** a fully blind benchmark.
- There is no authentication, deployment, durable recovery or idempotency, as allowed by the brief.

## Time spent

About **2 hours** in total on 19 October 2026:

- **About 40 min:** reading the brief, analysing the three CSVs (catalogue values, answer structure, sentence boundaries) and planning the design.
- **About 1 h 20 min:** setup, code, tests, the four live runs, the error analysis and this README.

The work stopped within the time limit. Unfinished items are listed under "Limitations and unfinished work".

## AI assistance and verification

**An AI coding assistant was used extensively.** It wrote most of the code, the prompts, the tests and this README, working under my direction in my local environment. I made these decisions:
- the provider (Gemini) and the setup (local PostgreSQL in Docker);
- the constraints on the repository and the submission;
- when to switch models after the quota and 404 errors;
- accepting the v2 change after reviewing the v1 error analysis.

**What was verified, with evidence in this repository:**
- **Data:** the SHA-256 hashes of the three CSVs match the issued files (`data/SHA256SUMS`). All 376 gold quotes equal `ai_answer[start:end]` when parsed with the csv module.
- **Sentence splitter:** it reproduces every one of the 376 development gold spans exactly. The decimal cases ("0.35 kg", "1.5 years") are covered by a test.
- **Tests:** all 46 tests were actually run, and they passed against a real PostgreSQL 16 (`runs/test_output.txt`). None were skipped.
- **Scorer:** it reproduces the worked example from the brief exactly: G=10, P=10, M=8, C=7 gives extraction 0.80 and joint 0.70.
- **Gold isolation:** a test asserts that no gold claim IDs, spans, explanations or label fields appear in any model or tool payload.
- **Live API:** `/classify` returned 200 with a real model call, 404 for an unknown brand, and 422 for a gold field or a bad UUID. `GET /evaluation-runs/{id}` returned the joined run (`runs/api_smoke.txt`).
- **Runs:** each of the four reported runs records prompt and source hashes. Both check runs share the frozen source hash with the final v2 development run.
- **Failures:** every failed or interrupted attempt is kept in `runs/` and in the database. None were deleted or used in the comparison.
- **Secrets:** the repository was searched for API keys, and none are present. The `.env` file is ignored by git.
