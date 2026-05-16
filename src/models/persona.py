from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Persona:
    """Represents a weighted UX research persona."""

    name: str
    weight: float
    color: str = "#4E79A7"
    radius: float = 1.0
    position: tuple[float, float] = (0.0, 0.0)
    topics: list[str] = field(default_factory=list)

    def add_topic(self, topic_name: str) -> None:
        if topic_name not in self.topics:
            self.topics.append(topic_name)
