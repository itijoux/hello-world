"""The live runner: turn a spread input dict into a validated SpreadOutput."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import anthropic

from .models import SpreadInput, SpreadOutput
from .prompt import build_output_schema, build_system_prompt, build_user_content

MODEL = "claude-opus-4-7"


@dataclass
class GenerationResult:
    output: SpreadOutput
    usage: Any  # anthropic Usage object
    raw_text: str


@dataclass
class DryRun:
    system: str
    user_content: str
    output_schema: dict


def _prepare(spread: dict) -> tuple[SpreadInput, str, str, dict]:
    data = SpreadInput.model_validate(spread)
    system = build_system_prompt(data.book_metadata)
    user_content = build_user_content(spread)
    schema = build_output_schema([p.id for p in data.photos])
    return data, system, user_content, schema


def dry_run(spread: dict) -> DryRun:
    """Build the prompt + schema without calling the API (for iteration)."""
    _, system, user_content, schema = _prepare(spread)
    return DryRun(system=system, user_content=user_content, output_schema=schema)


def generate_spread(
    spread: dict,
    *,
    client: anthropic.Anthropic | None = None,
    model: str = MODEL,
    effort: str = "high",
    max_tokens: int = 8000,
) -> GenerationResult:
    """Generate one spread via Claude, returning validated, schema-checked output."""
    data, system, user_content, schema = _prepare(spread)
    client = client or anthropic.Anthropic()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
        output_config={
            "effort": effort,
            "format": {"type": "json_schema", "schema": schema},
        },
    )

    if response.stop_reason == "refusal":
        detail = getattr(response, "stop_details", None)
        raise RuntimeError(f"Model refused to generate this spread: {detail}")

    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise RuntimeError(
            f"No text block in response (stop_reason={response.stop_reason}). "
            "If this is max_tokens, raise --max-tokens."
        )

    output = SpreadOutput.model_validate(json.loads(text))

    expected_ids = {p.id for p in data.photos}
    missing = expected_ids - set(output.captions)
    if missing:
        raise RuntimeError(f"Model omitted captions for photos: {sorted(missing)}")

    return GenerationResult(output=output, usage=response.usage, raw_text=text)
