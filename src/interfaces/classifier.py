"""
Classifier interface.

Categorises an incoming public comment into one of the system's routing
categories. The implementation is proprietary and not included in this
repository.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Protocol


class Category(str, Enum):
    GENERAL = "general"
    ABUSIVE = "abusive"
    DISMISSIVE_TROLL = "dismissive_troll"
    UNSUPPORTED_CLAIM = "unsupported_claim"
    SEEKING_HELP = "seeking_help"
    REFUSE_AND_DEFLECT = "refuse_and_deflect"
    NO_ACTION = "no_action"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class CommentInput:
    comment_id: str
    post_id: str
    author_id: str
    text: str
    language: Optional[str]
    is_reply: bool
    parent_post_age_minutes: int


@dataclass(frozen=True)
class ClassificationResult:
    category: Category
    confidence: Confidence
    mention_target: Optional[str]
    language: str
    injection_detected: bool
    refusal_required: bool


class Classifier(Protocol):
    def classify(self, comment: CommentInput) -> ClassificationResult: ...
