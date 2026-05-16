from __future__ import annotations

import csv
import json
from pathlib import Path

from matplotlib.figure import Figure

from src.models.overlap import Overlap


def ensure_parent_dir(output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def export_png(fig: Figure, output_path: str | Path, dpi: int = 180) -> Path:
    path = ensure_parent_dir(output_path)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def export_svg(fig: Figure, output_path: str | Path) -> Path:
    path = ensure_parent_dir(output_path)
    fig.savefig(path, bbox_inches="tight")
    return path


def export_priority_table(topics: list[dict[str, object]], output_path: str | Path) -> None:
    path = ensure_parent_dir(output_path)
    fieldnames = [
        "name",
        "type",
        "personas",
        "overlap_level",
        "accumulated_weight",
        "impact_score",
        "centrality",
    ]

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for topic in topics:
            row = dict(topic)
            row["personas"] = ";".join(str(persona) for persona in topic["personas"])
            writer.writerow({key: row.get(key) for key in fieldnames})


def export_csv(topics: list[dict[str, object]], output_path: str | Path) -> Path:
    export_priority_table(topics, output_path)
    return Path(output_path)


def export_overlaps_json(overlaps: list[Overlap], output_path: str | Path) -> None:
    path = ensure_parent_dir(output_path)
    payload = [
        {
            "personas": list(overlap.personas),
            "topics": [
                {
                    "name": topic.name,
                    "type": topic.type.value,
                    "overlap_level": topic.overlap_level,
                    "impact_score": topic.impact_score,
                }
                for topic in overlap.topics
            ],
            "accumulated_weight": overlap.accumulated_weight,
            "centrality": overlap.centrality,
        }
        for overlap in overlaps
    ]

    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def export_json(overlaps: list[Overlap], output_path: str | Path) -> Path:
    export_overlaps_json(overlaps, output_path)
    return Path(output_path)
