CREATE TABLE IF NOT EXISTS runs (
    id                UUID PRIMARY KEY,
    split             TEXT NOT NULL CHECK (split IN ('development', 'check', 'adhoc')),
    agent_version     TEXT NOT NULL CHECK (agent_version IN ('v1', 'v2')),
    prompt_hash       TEXT NOT NULL,
    source_hash       TEXT NOT NULL,
    source_revision   TEXT,
    dataset_version   TEXT NOT NULL,
    evaluator_version TEXT NOT NULL,
    fact_version      TEXT NOT NULL,
    provider          TEXT NOT NULL,
    model             TEXT NOT NULL,
    settings          JSONB NOT NULL,
    file_hashes       JSONB NOT NULL,
    status            TEXT NOT NULL CHECK (status IN ('running', 'completed', 'failed')),
    failure_reason    TEXT,
    counts            JSONB,
    metrics           JSONB,
    missed_gold_ids   JSONB,
    unmatched_prediction_ids JSONB,
    wrong_label_ids   JSONB,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at       TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS answer_results (
    run_id        UUID NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    answer_id     TEXT NOT NULL,
    seq           INTEGER NOT NULL,
    status        TEXT NOT NULL CHECK (status IN ('ok', 'error')),
    error_type    TEXT,
    error_message TEXT,
    claim_count   INTEGER NOT NULL,
    turns         INTEGER NOT NULL,
    latency_ms    INTEGER NOT NULL,
    trace_ref     TEXT,
    PRIMARY KEY (run_id, answer_id)
);

CREATE TABLE IF NOT EXISTS claim_results (
    run_id         UUID NOT NULL,
    answer_id      TEXT NOT NULL,
    claim_id       TEXT NOT NULL,
    start_char     INTEGER NOT NULL CHECK (start_char >= 0),
    end_char       INTEGER NOT NULL CHECK (end_char > start_char),
    quote          TEXT NOT NULL,
    label          TEXT NOT NULL CHECK (label IN ('supported', 'contradicted', 'unknown')),
    fact_ids       JSONB NOT NULL,
    reason         TEXT NOT NULL,
    matched_gold_id TEXT,
    gold_label     TEXT,
    label_correct  BOOLEAN,
    UNIQUE (run_id, answer_id, start_char, end_char),
    UNIQUE (run_id, claim_id),
    FOREIGN KEY (run_id, answer_id) REFERENCES answer_results(run_id, answer_id) ON DELETE CASCADE
);
