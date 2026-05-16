from __future__ import annotations

from math import dist


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return dist(a, b)


def circles_overlap(
    center_a: tuple[float, float],
    radius_a: float,
    center_b: tuple[float, float],
    radius_b: float,
) -> bool:
    return distance(center_a, center_b) <= radius_a + radius_b


def weighted_radius(weight: float, max_weight: float, min_radius: float = 1.2, max_radius: float = 2.8) -> float:
    if max_weight <= 0:
        return min_radius
    return min_radius + (weight / max_weight) ** 0.5 * (max_radius - min_radius)


def centroid(points: list[tuple[float, float]]) -> tuple[float, float]:
    if not points:
        return (0.0, 0.0)
    x = sum(point[0] for point in points) / len(points)
    y = sum(point[1] for point in points) / len(points)
    return (x, y)
