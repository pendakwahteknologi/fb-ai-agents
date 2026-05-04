"""
Throttler interface.

Enforces human-pace timing for replies and reactions, per-Page hourly caps,
and backoff on observed anti-spam responses. The exact bands, caps, jitter
curves, and skip rates are proprietary and not included in this repository.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

from .router import AgentId


@dataclass(frozen=True)
class ThrottleDecision:
    wait_seconds: float
    skip: bool
    reason_tag: str


class Throttler(Protocol):
    def reserve_reply_slot(self, agent: AgentId) -> ThrottleDecision: ...

    def reserve_reaction_slot(self, agent: AgentId) -> ThrottleDecision: ...

    def record_outcome(
        self,
        agent: AgentId,
        success: bool,
        error_code: int | None,
    ) -> None: ...
