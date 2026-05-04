"""
Poster interface.

Issues outbound Graph API calls under a specific persona Page's access
token. The only component holding write tokens. Token storage and
redaction are proprietary and not included in this repository.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

from .router import AgentId


@dataclass(frozen=True)
class PostResult:
    success: bool
    published_id: str | None
    error_code: int | None
    error_message: str | None


class Poster(Protocol):
    def post_reply(
        self,
        agent: AgentId,
        parent_comment_id: str,
        text: str,
    ) -> PostResult: ...

    def post_reaction(
        self,
        agent: AgentId,
        target_id: str,
    ) -> PostResult: ...

    def delete_published(
        self,
        agent: AgentId,
        published_id: str,
    ) -> PostResult: ...
