"""
State store interface.

Persists deduplication state, thread engagement state, and per-Page health.
All writes are atomic (temp file plus rename). The capping policy and
recovery procedure are proprietary and not included in this repository.
"""

from __future__ import annotations
from typing import Protocol

from .router import AgentId, PageHealth


class StateStore(Protocol):
    def is_processed(self, comment_id: str) -> bool: ...

    def mark_processed(self, comment_id: str) -> None: ...

    def is_engaged_thread(self, thread_root_id: str) -> bool: ...

    def mark_engaged_thread(self, thread_root_id: str, by_agent: AgentId) -> None: ...

    def get_page_health(self, agent: AgentId) -> PageHealth: ...

    def set_page_health(
        self,
        agent: AgentId,
        health: PageHealth,
        cooldown_seconds: int | None = None,
    ) -> None: ...
