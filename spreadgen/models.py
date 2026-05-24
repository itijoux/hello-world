"""Pydantic models for spread generation input and output.

Validation happens at the boundary (the input JSON the user hands us, and the
JSON Claude returns). Internal code trusts these models.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class _Lenient(BaseModel):
    # Real trip data carries fields we don't model yet; ignore them rather than
    # reject the whole spread.
    model_config = ConfigDict(extra="ignore")


class BookMetadata(_Lenient):
    trip_name: str
    total_days: int | None = None
    voice: str = "warm_editorial_observation"
    language: str = "fr"


class SpreadContext(_Lenient):
    spread_id: str
    chapter_title: str
    spread_type: str | None = None
    template: str | None = None


class Location(_Lenient):
    primary: str
    coordinates_center: list[float] | None = None
    neighborhood_context: str | None = None


class TimeInfo(_Lenient):
    start: str | None = None
    end: str | None = None
    duration_minutes: int | None = None
    time_of_day_label: str | None = None


class Photo(_Lenient):
    id: str
    role: str | None = None
    vision_tags: list[str] = Field(default_factory=list)
    scene_type: str | None = None
    time_of_day: str | None = None
    quality: str | None = None


class UserGroundTruth(_Lenient):
    memo_id: str | None = None
    attached_to_photos: list[str] = Field(default_factory=list)
    transcript: str


class SpreadInput(_Lenient):
    book_metadata: BookMetadata
    previous_chapter_closing: str | None = None
    spread_context: SpreadContext
    location: Location
    time: TimeInfo | None = None
    photos: list[Photo] = Field(default_factory=list)
    user_ground_truth: UserGroundTruth | None = None


class SpreadOutput(BaseModel):
    """The strict JSON Claude is constrained to return."""

    model_config = ConfigDict(extra="forbid")

    headline: str
    lede: str
    body: str
    captions: dict[str, str]
    closing_line: str
