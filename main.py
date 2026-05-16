from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.processing.impact_score import calculate_impact_scores
from src.processing.overlap_calculator import calculate_overlaps
from src.processing.parser import load_research_csv
from src.visualization.export import export_csv, export_json, export_png, export_svg
from src.visualization.export_html import export_interactive_html
from src.visualization.renderer import render_weighted_persona_map
from src.visualization.renderer_plotly import render_interactive_persona_map


DEFAULT_OUTPUT_DIRS = {
    "png": Path("data/outputs/diagrams/weighted_persona_map.png"),
    "svg": Path("data/outputs/diagrams/weighted_persona_map.svg"),
    "html": Path("data/outputs/diagrams/weighted_persona_map.html"),
    "csv": Path("data/outputs/tables/topic_priorities.csv"),
    "json": Path("data/processed/overlaps.json"),
}


def ensure_output_dirs() -> None:
    """Ensure output directories exist."""

    for output_path in DEFAULT_OUTPUT_DIRS.values():
        output_path.parent.mkdir(parents=True, exist_ok=True)


def validate_csv_path(raw_path: str) -> Path:
    path = Path(raw_path.strip().strip('"')).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    if not path.is_file():
        raise ValueError(f"CSV path is not a file: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Input file must be a .csv: {path}")

    return path


def prompt_csv_path() -> Path:
    while True:
        try:
            raw_path = input("Enter research CSV path:\n> ")
            return validate_csv_path(raw_path)
        except (FileNotFoundError, ValueError) as error:
            print(f"Invalid input: {error}")
            print('Expected a file path, for example: "C:\\path\\research.csv"')


def print_top_priorities(scored_topics: list[dict[str, object]], limit: int = 5) -> None:
    print("Top priorities:")
    for topic in scored_topics[:limit]:
        print(f"- {topic['name']} (score={topic['impact_score']:.2f})")


def export_selected_outputs(personas, topics, selected_formats: list[str]) -> list[Path]:
    overlaps = calculate_overlaps(topics, personas)
    scored_topics = calculate_impact_scores(overlaps)
    scored_topics = sorted(
        scored_topics,
        key=lambda topic: topic["impact_score"],
        reverse=True,
    )

    exported_paths: list[Path] = []
    fig = render_weighted_persona_map(
        personas=personas,
        topics=scored_topics,
        interactive_controls=False,
    )

    try:
        if "png" in selected_formats:
            path = export_png(fig, DEFAULT_OUTPUT_DIRS["png"])
            exported_paths.append(path)
            print(f"PNG exported to: {path}")

        if "svg" in selected_formats:
            path = export_svg(fig, DEFAULT_OUTPUT_DIRS["svg"])
            exported_paths.append(path)
            print(f"SVG exported to: {path}")

        if "html" in selected_formats:
            plotly_fig = render_interactive_persona_map(personas, scored_topics)
            path = export_interactive_html(plotly_fig, DEFAULT_OUTPUT_DIRS["html"])
            exported_paths.append(path)
            print(f"HTML exported to: {path}")

        if "csv" in selected_formats:
            path = export_csv(scored_topics, DEFAULT_OUTPUT_DIRS["csv"])
            exported_paths.append(path)
            print(f"CSV exported to: {path}")

        if "json" in selected_formats:
            path = export_json(overlaps, DEFAULT_OUTPUT_DIRS["json"])
            exported_paths.append(path)
            print(f"JSON exported to: {path}")

        return exported_paths
    finally:
        plt.close(fig)


def main() -> None:
    """Run the interactive framework workflow."""

    print("=" * 60)
    print("WEIGHTED PERSONA CONVERGENCE FRAMEWORK")
    print("=" * 60)

    ensure_output_dirs()

    research_csv = prompt_csv_path()

    print("\nLoading research data...")
    personas, topics = load_research_csv(research_csv)

    print(f"Loaded {len(personas)} personas inferred from Pessoa")
    print(f"Loaded {len(topics)} topics from Elemento")

    print("\nCalculating overlaps...")
    overlaps = calculate_overlaps(topics, personas)
    print(f"Generated {len(overlaps)} overlaps")

    print("\nCalculating impact scores...")
    scored_topics = calculate_impact_scores(overlaps)
    scored_topics = sorted(
        scored_topics,
        key=lambda topic: topic["impact_score"],
        reverse=True,
    )
    print_top_priorities(scored_topics)

    print("\nRendering visualization...")
    fig = render_weighted_persona_map(
        personas=personas,
        topics=scored_topics,
        export_callback=lambda selected_formats: export_selected_outputs(
            personas,
            topics,
            selected_formats,
        ),
    )

    print("\nPreview window opened. Use Export inside the preview to save files.")
    plt.show()

    overlaps = calculate_overlaps(topics, personas)
    scored_topics = calculate_impact_scores(overlaps)
    scored_topics = sorted(
        scored_topics,
        key=lambda topic: topic["impact_score"],
        reverse=True,
    )
    print("\nUpdated priorities after weight adjustment:")
    print_top_priorities(scored_topics)

    plt.close(fig)

    print("\nFramework execution completed successfully.")


if __name__ == "__main__":
    main()
