from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go

from src.visualization.export import ensure_parent_dir


def export_interactive_html(fig: go.Figure, output_path: str | Path) -> Path:
    path = ensure_parent_dir(output_path)
    fig.write_html(
        path,
        include_plotlyjs=True,
        full_html=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": True,
            "toImageButtonOptions": {"format": "png", "scale": 2},
        },
    )
    return path
