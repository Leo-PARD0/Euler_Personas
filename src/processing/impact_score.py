from __future__ import annotations

from src.models.overlap import Overlap


def calculate_impact_scores(overlaps: list[Overlap]) -> list[dict[str, object]]:
    scored_topics: list[dict[str, object]] = []

    for overlap in overlaps:
        overlap_frequency = overlap.overlap_level
        for topic in overlap.topics:
            topic.impact_score = overlap.accumulated_weight * overlap_frequency
            topic.overlap_level = overlap.overlap_level
            scored_topics.append(
                {
                    "name": topic.name,
                    "type": topic.type.value,
                    "personas": list(overlap.personas),
                    "overlap_level": topic.overlap_level,
                    "impact_score": topic.impact_score,
                    "accumulated_weight": overlap.accumulated_weight,
                    "centrality": overlap.centrality,
                }
            )

    return scored_topics
