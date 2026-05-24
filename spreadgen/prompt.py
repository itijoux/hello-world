"""Builds the system prompt, user content, and per-spread output schema.

The system prompt is frozen per (voice, language) so it can be prompt-cached
across spreads. Anything that varies per spread (the spread JSON, the previous
chapter's closing line) goes in the user turn.
"""

from __future__ import annotations

import json

from .models import BookMetadata

# Voice keys map to a concrete instruction block. Add new voices here.
_VOICES = {
    "warm_editorial_observation": (
        "Warm editorial observation. Third person. Past tense. Literary but "
        "never pretentious. Think of a thoughtful travel writer describing "
        "someone else's experience — observed, dignified, specific."
    ),
}

# Cliché words to ban, per output language. The model writes in the book's
# language, so the negative list must be in that language to actually bite.
_CLICHES = {
    "fr": [
        "magique", "inoubliable", "incroyable", "vibrant", "découverte",
        "dépaysement", "authentique", "pittoresque", "charmant", "féerique",
    ],
    "en": [
        "magical", "unforgettable", "incredible", "vibrant", "hidden gem",
        "journey", "discovery", "authentic", "picturesque", "charming",
        "nestled", "bustling",
    ],
}

# First/second-person pronouns to forbid, per language (voice is third person).
_PERSON_BANS = {
    "fr": 'Do not write in the first person ("nous", "j\'ai", "on") or address '
          'the reader as "vous".',
    "en": "Do not write in the first person (\"we\", \"I\") or address the "
          "reader as \"you\".",
}


def _language_name(code: str) -> str:
    return {"fr": "French", "en": "English"}.get(code, code)


def build_system_prompt(meta: BookMetadata) -> str:
    lang = meta.language
    voice = _VOICES.get(meta.voice, _VOICES["warm_editorial_observation"])
    cliches = _CLICHES.get(lang, _CLICHES["en"])
    person_ban = _PERSON_BANS.get(lang, _PERSON_BANS["en"])

    return f"""You are an editor writing one spread of a personal travel book in {_language_name(lang)}.

VOICE: {voice}

GROUND TRUTH HIERARCHY (strict, in priority order):
1. user_ground_truth.transcript -> HIGHEST priority. Names, facts, relationships,
   places, and feelings the user mentioned MUST appear in the text. Do not
   generalize away from specifics. If the memo says "his wife lived in Marseille
   in the 90s", that detail goes in. The narrative is about what the memo says,
   even when the photos show something else.
2. photo vision_tags -> SECONDARY. Use only to add visual texture around what the
   memo already establishes. Never invent a story from the tags alone.
3. EXIF, location, and time -> CONTEXT ONLY, never the subject of the writing.

CONTINUITY: If a previous chapter's closing line is provided, your opening should
feel like a natural successor to it — a continuation of the same voice and thread,
not a hard reset. If none is provided, open the book/chapter cleanly.

NEVER:
- Invent names, relationships, or biographical details not present in the memo.
- Describe events or emotions the ground truth does not support.
- Use these clichés: {", ".join(cliches)}.
- Use exclamation marks.
- {person_ban}

OUTPUT: Return ONLY a JSON object with exactly these fields, written in {_language_name(lang)}:
- "headline": max 4 words.
- "lede": one sentence, max 20 words — the opening line of the spread.
- "body": the main paragraph, 90-110 words, anchored in the memo.
- "captions": an object with one entry per photo id; each caption is max 12 words,
  factual and textured.
- "closing_line": one sentence, max 18 words, a transition toward what comes next.
"""


def build_user_content(spread: dict) -> str:
    """The per-spread turn: the spread payload, plus an explicit continuity nudge."""
    payload = json.dumps(spread, ensure_ascii=False, indent=2)
    prev = (spread.get("previous_chapter_closing") or "").strip()

    parts = ["Write the spread for the following input.\n"]
    if prev:
        parts.append(
            f'The previous chapter closed with: "{prev}"\n'
            "Open this spread as a natural successor to that line.\n"
        )
    parts.append(f"\nSPREAD INPUT:\n{payload}")
    return "".join(parts)


def build_output_schema(photo_ids: list[str]) -> dict:
    """A strict JSON schema whose caption keys are exactly this spread's photo ids.

    Generating the schema per-spread is what lets us guarantee a caption for
    every photo while keeping the caller's desired shape (captions keyed by id).
    Length limits ("max 4 words" etc.) are enforced via the prompt, not the
    schema — structured outputs don't support string-length constraints.
    """
    caption_props = {pid: {"type": "string"} for pid in photo_ids}
    return {
        "type": "object",
        "properties": {
            "headline": {"type": "string"},
            "lede": {"type": "string"},
            "body": {"type": "string"},
            "captions": {
                "type": "object",
                "properties": caption_props,
                "required": list(photo_ids),
                "additionalProperties": False,
            },
            "closing_line": {"type": "string"},
        },
        "required": ["headline", "lede", "body", "captions", "closing_line"],
        "additionalProperties": False,
    }
