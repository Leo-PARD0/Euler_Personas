from __future__ import annotations

from html import escape

from src.models.persona import Persona


def build_topic_tooltip(topic: dict[str, object]) -> str:
    topic_type = escape(str(topic["type"]))
    topic_name = escape(str(topic["name"]))
    personas = [escape(str(persona)) for persona in topic["personas"]]

    shared_by = "<br>".join(f"- {persona}" for persona in personas)
    return (
        f"<b>{topic_type}</b>"
        "<br>--------------------------------"
        f"<br>{topic_name}"
        "<br><br><b>Shared by:</b>"
        f"<br>{shared_by}"
        f"<br><br><b>Impact Score:</b> {float(topic['impact_score']):.2f}"
    )


def build_persona_tooltip(persona: Persona, topics: list[dict[str, object]]) -> str:
    persona_topics = [
        topic
        for topic in topics
        if persona.name in {str(name) for name in topic["personas"]}
    ]
    exclusive_topics = [
        topic
        for topic in persona_topics
        if len(topic["personas"]) == 1
    ]

    exclusive_text = "<br>".join(
        f"- {escape(str(topic['name']))}"
        for topic in exclusive_topics[:8]
    )
    if not exclusive_text:
        exclusive_text = "None"

    return (
        f"<b>{escape(persona.name)}</b>"
        f"<br>Representativity: {persona.weight:.2f}%"
        f"<br>Total topics: {len(persona_topics)}"
        "<br><br><b>Exclusive topics:</b>"
        f"<br>{exclusive_text}"
    )
