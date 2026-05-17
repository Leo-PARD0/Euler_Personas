from __future__ import annotations

from src.models.overlap import Overlap


def calculate_impact_scores(overlaps: list[Overlap]) -> list[dict[str, object]]:
    """Calculate impact scores based on topic representativity.
    
    Topic-centric model: impact_score = topic.representativity * overlap_level
    where overlap_level represents semantic density (number of personas sharing the topic).
    """
    scored_topics: list[dict[str, object]] = []

    for overlap in overlaps:
        for topic in overlap.topics:
            # NEW: impact_score derived from topic representativity
            # Multiply by overlap_level for topics shared across many personas
            topic.impact_score = topic.representativity * (overlap.overlap_level / 10.0)
            topic.overlap_level = overlap.overlap_level
            
            scored_topics.append(
                {
                    "name": topic.name,
                    "type": topic.type.value,
                    "personas": list(overlap.personas),
                    "representativity": topic.representativity,  # NEW: include raw representativity
                    "overlap_level": topic.overlap_level,
                    "impact_score": topic.impact_score,
                    "evidence": topic.evidence,  # NEW: include evidence
                }
            )

    return scored_topics
