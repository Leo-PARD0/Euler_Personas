from __future__ import annotations

from collections import defaultdict

from src.models.overlap import Overlap
from src.models.persona import Persona
from src.models.topic import Topic


def calculate_overlaps(topics: list[Topic], personas: list[Persona]) -> list[Overlap]:
    persona_weights = {persona.name: persona.weight for persona in personas}
    persona_lookup = {persona.name: persona for persona in personas}
    grouped_topics: dict[tuple[str, ...], list[Topic]] = defaultdict(list)

    for topic in topics:
        key = tuple(sorted(topic.personas))
        grouped_topics[key].append(topic)
        for persona_name in topic.personas:
            if persona_name not in persona_lookup:
                raise ValueError(f"Topic '{topic.name}' references unknown persona '{persona_name}'")
            persona_lookup[persona_name].add_topic(topic.name)

    overlaps: list[Overlap] = []
    max_personas = max((len(persona_names) for persona_names in grouped_topics), default=1)
    for persona_names, shared_topics in grouped_topics.items():
        accumulated_weight = sum(persona_weights[name] for name in persona_names)
        centrality = len(persona_names) / max_personas
        overlaps.append(
            Overlap(
                personas=persona_names,
                topics=shared_topics,
                accumulated_weight=accumulated_weight,
                centrality=centrality,
            )
        )

    return sorted(overlaps, key=lambda item: (item.overlap_level, item.accumulated_weight), reverse=True)
