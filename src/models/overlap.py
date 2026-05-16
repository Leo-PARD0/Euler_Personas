from __future__ import annotations

from dataclasses import dataclass, field

from src.models.topic import Topic


@dataclass(slots=True)
class Overlap:
    """Represents the shared region created by two or more personas."""

    personas: tuple[str, ...]
    topics: list[Topic] = field(default_factory=list)
    accumulated_weight: float = 0.0
    centrality: float = 0.0

    @property
    def overlap_level(self) -> int:
        return len(self.personas)

    @property
    def topic_names(self) -> list[str]:
        return [topic.name for topic in self.topics]
