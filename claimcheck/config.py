"""Settings and version constants. Values come from the environment (or a local .env)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PROMPTS_DIR = ROOT / "prompts"
RUNS_DIR = ROOT / "runs"

DATASET_VERSION = "long-brand-answers-50-v4"
FACT_VERSION = "speaker-catalogue-v4"
EVALUATOR_VERSION = "sentence-spans-and-labels-v4"
AGENT_VERSIONS = ("v1", "v2")
LABELS = ("supported", "contradicted", "unknown")
MAX_MODEL_TURNS = 3


def _load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "gemini"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gemini-3.5-flash-lite"))
    base_url: str = field(
        default_factory=lambda: os.getenv(
            "LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    )
    api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    # Per provider request timeout in seconds (documented in README).
    request_timeout_s: float = field(default_factory=lambda: float(os.getenv("LLM_TIMEOUT_S", "120")))
    temperature: float = field(default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0")))
    # Retries for rate-limit / transient 5xx responses only; never counted as model turns.
    transient_retries: int = field(default_factory=lambda: int(os.getenv("LLM_TRANSIENT_RETRIES", "6")))
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))

    def public(self) -> dict:
        """Settings safe to store in run metadata (no secrets)."""
        return {
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
            "request_timeout_s": self.request_timeout_s,
            "temperature": self.temperature,
            "transient_retries": self.transient_retries,
            "max_model_turns": MAX_MODEL_TURNS,
        }


def get_settings() -> Settings:
    return Settings()
