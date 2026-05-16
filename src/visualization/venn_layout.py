from __future__ import annotations

from math import cos, pi, sin, sqrt

from src.models.persona import Persona
from src.utils.geometry import centroid, distance, weighted_radius


def assign_weighted_circle_layout(personas: list[Persona]) -> list[Persona]:
    if not personas:
        return personas

    for persona in personas:
        persona.radius = weighted_radius(persona.weight, 100)

    smallest_radius = min(persona.radius for persona in personas)
    layout_radius = smallest_radius * 0.62
    count = len(personas)

    if count == 1:
        personas[0].position = (0.0, 0.0)
        return personas

    for index, persona in enumerate(personas):
        angle = 2 * pi * index / count
        persona.position = (layout_radius * cos(angle), layout_radius * sin(angle))

    return personas


def persona_label_position(persona: Persona, personas: list[Persona]) -> tuple[float, float]:
    """Place persona labels on an invisible regular polygon around the map."""

    max_radius = max((item.radius for item in personas), default=1.0)
    polygon_radius = max(
        sqrt(persona.position[0] ** 2 + persona.position[1] ** 2)
        for persona in personas
    ) + max_radius + 0.7

    x, y = persona.position
    if x == 0 and y == 0:
        return (0.0, polygon_radius)

    length = sqrt(x**2 + y**2)
    return (x / length * polygon_radius, y / length * polygon_radius)


def topic_position(
    persona_names: list[str],
    personas: list[Persona],
    index: int = 0,
    total: int = 1,
) -> tuple[float, float]:
    lookup = {persona.name: persona for persona in personas}
    involved = [lookup[name] for name in persona_names if name in lookup]
    excluded = [persona for persona in personas if persona.name not in set(persona_names)]

    if not involved:
        return (0.0, 0.0)

    target = _region_target(involved, excluded)
    target = _spread_target(target, index, total, involved)

    exclusive = _best_candidate(target, involved, excluded, require_outside_excluded=True)
    if exclusive is not None:
        return exclusive

    fallback = _best_candidate(target, involved, excluded, require_outside_excluded=False)
    if fallback is not None:
        return fallback

    return centroid([persona.position for persona in involved])


def _point_inside_all(point: tuple[float, float], personas: list[Persona]) -> bool:
    return all(distance(point, persona.position) <= persona.radius for persona in personas)


def _region_target(involved: list[Persona], excluded: list[Persona]) -> tuple[float, float]:
    if len(excluded) == 0:
        return (0.0, 0.0)

    involved_centroid = centroid([persona.position for persona in involved])
    excluded_centroid = centroid([persona.position for persona in excluded])

    if len(involved) == 1:
        persona = involved[0]
        direction = _unit_vector(persona.position)
        return (
            persona.position[0] + direction[0] * persona.radius * 0.45,
            persona.position[1] + direction[1] * persona.radius * 0.45,
        )

    away = _unit_vector(
        (
            involved_centroid[0] - excluded_centroid[0],
            involved_centroid[1] - excluded_centroid[1],
        )
    )
    smallest_radius = min(persona.radius for persona in involved)
    return (
        involved_centroid[0] + away[0] * smallest_radius * 0.35,
        involved_centroid[1] + away[1] * smallest_radius * 0.35,
    )


def _spread_target(
    target: tuple[float, float],
    index: int,
    total: int,
    involved: list[Persona],
) -> tuple[float, float]:
    if total <= 1:
        return target

    smallest_radius = min(persona.radius for persona in involved)
    angle = 2 * pi * index / total
    radius = min(0.22 * smallest_radius, 0.42)
    return (target[0] + cos(angle) * radius, target[1] + sin(angle) * radius)


def _best_candidate(
    target: tuple[float, float],
    involved: list[Persona],
    excluded: list[Persona],
    require_outside_excluded: bool,
) -> tuple[float, float] | None:
    all_personas = involved + excluded
    extent = max(
        abs(coord) + persona.radius
        for persona in all_personas
        for coord in persona.position
    )
    steps = 42
    grid_min = -extent
    step = (extent * 2) / steps

    best_point = None
    best_score = float("inf")

    for x_index in range(steps + 1):
        x = grid_min + x_index * step
        for y_index in range(steps + 1):
            y = grid_min + y_index * step
            point = (x, y)

            if not _point_inside_all(point, involved):
                continue
            if require_outside_excluded and _point_inside_any(point, excluded):
                continue

            score = distance(point, target)
            if not require_outside_excluded:
                score += sum(
                    max(0.0, persona.radius - distance(point, persona.position))
                    for persona in excluded
                ) * 3

            if score < best_score:
                best_score = score
                best_point = point

    return best_point


def _point_inside_any(point: tuple[float, float], personas: list[Persona]) -> bool:
    return any(distance(point, persona.position) <= persona.radius for persona in personas)


def _unit_vector(vector: tuple[float, float]) -> tuple[float, float]:
    x, y = vector
    length = sqrt(x**2 + y**2)
    if length == 0:
        return (0.0, 1.0)
    return (x / length, y / length)
