from __future__ import annotations

from pathlib import Path
import re

import pandas as pd

from src.models.persona import Persona
from src.models.topic import Topic, TopicType
from src.utils.colors import persona_color


COLUMN_ALIASES = {
    "topic": {"topic", "topico", "tópico", "elemento", "dor", "objetivo"},
    "type": {"type", "tipo", "categoria"},
    "persona": {"persona"},
    "personas": {"personas", "pessoa", "pessoas"},
    "weight": {"weight", "peso", "representatividade", "representatividade (%)"},
    "evidence": {"evidence", "origem", "origem do dado", "fonte"},
}

TYPE_ALIASES = {
    "pain": TopicType.PAIN_POINT,
    "pain point": TopicType.PAIN_POINT,
    "painpoint": TopicType.PAIN_POINT,
    "dor": TopicType.PAIN_POINT,
    "dores": TopicType.PAIN_POINT,
    "goal": TopicType.GOAL,
    "objetivo": TopicType.GOAL,
    "objetivos": TopicType.GOAL,
}


def _require_columns(frame: pd.DataFrame, required: set[str], file_path: str | Path) -> None:
    missing = required.difference(frame.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"{file_path} is missing required columns: {missing_text}")


def _normalize_text(value: object) -> str:
    return str(value).strip()


def _normalize_column_name(column: str) -> str:
    clean = column.strip().lower()
    for canonical_name, aliases in COLUMN_ALIASES.items():
        if clean in aliases:
            return canonical_name
    return clean


def _read_csv(file_path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(file_path)
    frame = frame.rename(columns={column: _normalize_column_name(column) for column in frame.columns})
    return frame


def _parse_persona_names(value: object) -> tuple[str, ...]:
    names = [
        item.strip()
        for item in re.split(r"[;,]", str(value))
        if item.strip()
    ]
    return tuple(dict.fromkeys(names))


def _parse_topic_type(value: object) -> TopicType:
    clean = str(value).strip().lower()
    if clean in {member.value.lower() for member in TopicType}:
        return TopicType(str(value).strip())
    if clean in TYPE_ALIASES:
        return TYPE_ALIASES[clean]
    raise ValueError(f"Invalid topic type '{value}'. Expected Pain Point/Pain or Objetivo/Goal.")


def _parse_representativity(value: object) -> float:
    """Parse representativity % handling Brazilian format (comma as decimal separator)."""
    if pd.isna(value):
        return 0.0
    
    text = str(value).strip()
    # Remove % symbol if present
    text = text.replace("%", "").strip()
    # Convert Brazilian format (90,30) to standard (90.30)
    text = text.replace(",", ".")
    
    try:
        result = float(text)
        # Clamp to 0-100 range
        return max(0.0, min(100.0, result))
    except ValueError:
        raise ValueError(f"Invalid representativity value '{value}'. Expected a number (e.g., '90,30%' or '90.30')")


def load_personas(file_path: str | Path) -> list[Persona]:
    frame = _read_csv(file_path)
    _require_columns(frame, {"persona", "weight"}, file_path)

    personas: list[Persona] = []
    for index, row in frame.iterrows():
        name = str(row["persona"]).strip()
        if not name:
            raise ValueError(f"Empty persona name at row {index + 2}")

        weight = float(row["weight"])
        if weight <= 0:
            raise ValueError(f"Persona '{name}' must have a positive weight")

        personas.append(Persona(name=name, weight=weight, color=persona_color(index)))

    return personas


def load_topics(file_path: str | Path) -> list[Topic]:
    frame = _read_csv(file_path)
    _require_columns(frame, {"topic", "type", "personas"}, file_path)

    topics: list[Topic] = []
    for index, row in frame.iterrows():
        name = _normalize_text(row["topic"])
        topic_type = _parse_topic_type(row["type"])
        personas = _parse_persona_names(row["personas"])

        if not name:
            raise ValueError(f"Empty topic name at row {index + 2}")
        if not personas:
            raise ValueError(f"Topic '{name}' must reference at least one persona")

        topics.append(
            Topic(
                name=name,
                type=topic_type,
                personas=personas,
                overlap_level=len(personas),
            )
        )

    return topics


def load_research_csv(file_path: str | Path) -> tuple[list[Persona], list[Topic]]:
    """Load research CSV with topic-centric model.
    
    CSV structure: Elemento, Tipo, Pessoa, Representatividade (%), Origem do Dado
    
    Returns derived personas with weights calculated as average of related topic representativities.
    """

    frame = _read_csv(file_path)
    _require_columns(frame, {"topic", "type", "personas"}, file_path)

    topics: list[Topic] = []
    persona_names: set[str] = set()
    persona_topics: dict[str, list[float]] = {}  # persona -> [representativities]

    for index, row in frame.iterrows():
        name = _normalize_text(row["topic"])
        topic_type = _parse_topic_type(row["type"])
        personas = _parse_persona_names(row["personas"])
        
        # Read representativity (new field)
        representativity = _parse_representativity(row.get("weight", 0.0))
        
        # Read evidence/origin (optional)
        evidence = _normalize_text(row.get("evidence", "")) if "evidence" in row else ""

        if not name:
            raise ValueError(f"Empty topic/element name at row {index + 2}")
        if not personas:
            raise ValueError(f"Topic '{name}' must reference at least one person/persona")

        persona_names.update(personas)
        
        # Track representativity for each persona
        for persona in personas:
            if persona not in persona_topics:
                persona_topics[persona] = []
            persona_topics[persona].append(representativity)

        topics.append(
            Topic(
                name=name,
                type=topic_type,
                personas=personas,
                representativity=representativity,
                overlap_level=len(personas),
                evidence=evidence,
            )
        )

    # Create personas with derived weights (average of their topics' representativities)
    personas = []
    for index, persona_name in enumerate(sorted(persona_names)):
        topic_representativities = persona_topics.get(persona_name, [0.0])
        derived_weight = sum(topic_representativities) / len(topic_representativities)
        
        personas.append(
            Persona(
                name=persona_name,
                weight=derived_weight,
                color=persona_color(index),
            )
        )

    return personas, topics
