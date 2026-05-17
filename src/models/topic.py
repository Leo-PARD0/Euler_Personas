from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TopicType(str, Enum):
    PAIN_POINT = "Pain"
    GOAL = "Goal"


@dataclass(slots=True)
class Topic:
    """Represents a qualitative pain point or goal with observed representativity.
    
    Core principle: Topics are the primary unit of analysis.
    - representativity: observed % from research data
    - impact_score: derived from representativity (now = representativity * overlap_level)
    - personas: contextual semantic mapping only
    """

    name: str
    type: TopicType
    personas: tuple[str, ...]
    representativity: float = 0.0  # observed % from research data
    overlap_level: int = 1
    impact_score: float = 0.0
    evidence: str = ""  # qualitative origin/source
    normalized_weight: float = 0.0  # for display/visualization

    @property
    def is_shared(self) -> bool:
        return self.overlap_level > 1
