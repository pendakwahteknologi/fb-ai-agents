"""
Router interface.

Maps a classified comment to a specific persona agent, considering Page
health, priority signals, and fallback paths. The fallback mechanism is
proprietary and not included in this repository.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Protocol

from .classifier import ClassificationResult, CommentInput


class AgentId(str, Enum):
    ADILA = "adila"
    HAKIMAH = "hakimah"
    AQILAH = "aqilah"
    HIDAYAH = "hidayah"


class Priority(str, Enum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"


class PageHealth(str, Enum):
    LIVE = "live"
    THROTTLED = "throttled"
    BLOCKED = "blocked"
    RECOVERING = "recovering"
    PAGE_IN_PREPARATION = "page_in_preparation"


@dataclass(frozen=True)
class RoutingDecision:
    selected_agent: AgentId
    priority: Priority
    mode_hint: Optional[str]
    rationale_tag: str
    fallback_used: bool


class Router(Protocol):
    def route(
        self,
        comment: CommentInput,
        classification: ClassificationResult,
        page_health: dict[AgentId, PageHealth],
    ) -> Optional[RoutingDecision]: ...
