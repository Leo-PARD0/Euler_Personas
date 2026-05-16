from __future__ import annotations

from collections import defaultdict

from src.models.topic import Topic


def group_topics_by_type(topics: list[Topic]) -> dict[str, list[Topic]]:
    grouped: dict[str, list[Topic]] = defaultdict(list)
    for topic in topics:
        grouped[topic.type.value].append(topic)
    return dict(grouped)
