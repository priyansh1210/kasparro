"""Model providers. The live provider talks to any OpenAI-compatible Chat Completions
endpoint (configured for Gemini); the fake provider replays scripted turns in tests."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Callable, Protocol

from .config import Settings


class ProviderError(Exception):
    error_type = "provider_error"


class ProviderTimeout(ProviderError):
    error_type = "provider_timeout"


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: str | None


@dataclass
class ModelTurn:
    content: str | None
    tool_calls: list[ToolCall]
    # message dict to append back into the conversation (keeps provider extras such as
    # thought signatures needed by some models for multi-turn tool use)
    message: dict
    usage: dict = field(default_factory=dict)


class Provider(Protocol):
    name: str
    model: str

    def complete(self, messages: list[dict], tools: list[dict]) -> ModelTurn: ...


class OpenAICompatProvider:
    def __init__(self, settings: Settings):
        from openai import OpenAI

        if not settings.api_key:
            raise ProviderError("no API key configured (set GEMINI_API_KEY)")
        self.name = settings.provider
        self.model = settings.model
        self.settings = settings
        # max_retries=0: transient retries are handled below so they are explicit and logged
        self.client = OpenAI(api_key=settings.api_key, base_url=settings.base_url,
                             timeout=settings.request_timeout_s, max_retries=0)

    def complete(self, messages: list[dict], tools: list[dict]) -> ModelTurn:
        import openai

        delay = 5.0
        for attempt in range(self.settings.transient_retries + 1):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model, messages=messages, tools=tools,
                    temperature=self.settings.temperature,
                    timeout=self.settings.request_timeout_s,
                )
                break
            except openai.APITimeoutError:
                raise ProviderTimeout(
                    f"provider request exceeded {self.settings.request_timeout_s:.0f}s timeout") from None
            except (openai.RateLimitError, openai.InternalServerError, openai.APIConnectionError) as exc:
                if attempt >= self.settings.transient_retries:
                    raise ProviderError(f"provider unavailable after retries: {type(exc).__name__}") from None
                time.sleep(delay)
                delay = min(delay * 2, 60)
            except openai.APIStatusError as exc:
                raise ProviderError(f"provider returned HTTP {exc.status_code}") from None
        if not resp.choices:
            raise ProviderError("provider returned no choices")
        msg = resp.choices[0].message
        calls = [ToolCall(tc.id, tc.function.name, tc.function.arguments) for tc in (msg.tool_calls or [])]
        message = msg.model_dump(exclude_none=True)
        message["role"] = "assistant"
        usage = resp.usage.model_dump(exclude_none=True) if resp.usage else {}
        return ModelTurn(msg.content, calls, message, usage)


class FakeProvider:
    """Scripted provider for tests. Each script step is either a ModelTurn, an exception
    instance to raise, or a callable(messages) -> ModelTurn. Every payload is recorded."""

    def __init__(self, script: list, name: str = "fake", model: str = "fake-model"):
        self.script = list(script)
        self.name = name
        self.model = model
        self.payloads: list[dict] = []

    def complete(self, messages: list[dict], tools: list[dict]) -> ModelTurn:
        self.payloads.append(json.loads(json.dumps({"messages": messages, "tools": tools}, default=str)))
        if not self.script:
            raise AssertionError("fake provider script exhausted")
        step = self.script.pop(0)
        if isinstance(step, Exception):
            raise step
        if isinstance(step, Callable) and not isinstance(step, ModelTurn):
            return step(messages)
        return step


def tool_turn(*brands: str, name: str = "get_brand_facts") -> ModelTurn:
    calls = [ToolCall(f"call_{i}", name, json.dumps({"brand_id": b})) for i, b in enumerate(brands)]
    message = {"role": "assistant", "content": None, "tool_calls": [
        {"id": c.id, "type": "function", "function": {"name": c.name, "arguments": c.arguments}}
        for c in calls]}
    return ModelTurn(None, calls, message)


def final_turn(payload: dict | str) -> ModelTurn:
    content = payload if isinstance(payload, str) else json.dumps(payload)
    return ModelTurn(content, [], {"role": "assistant", "content": content})


def build_provider(settings: Settings) -> Provider:
    return OpenAICompatProvider(settings)
