from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TopicType(str, Enum):
    PAIN_POINT = "Pain"
    GOAL = "Goal"


@dataclass(slots=True)
class Topic:
    """Represents a qualitative pain point or goal mapped to personas."""

    name: str
    type: TopicType
    personas: tuple[str, ...]
    overlap_level: int = 1
    impact_score: float = 0.0

    @property
    def is_shared(self) -> bool:
        return self.overlap_level > 1
