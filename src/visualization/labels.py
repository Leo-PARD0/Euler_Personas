from __future__ import annotations


def stagger_label_position(
    base_position: tuple[float, float],
    index: int,
    step: float = 0.18,
) -> tuple[float, float]:
    x, y = base_position
    direction = -1 if index % 2 else 1
    return (x, y + direction * step * ((index + 1) // 2))
