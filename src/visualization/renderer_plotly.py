from __future__ import annotations

from collections import defaultdict

import plotly.graph_objects as go

from src.models.persona import Persona
from src.utils.colors import topic_color
from src.visualization.tooltip_builder import build_persona_tooltip, build_topic_tooltip
from src.visualization.venn_layout import persona_label_position, topic_position


def render_interactive_persona_map(
    personas: list[Persona],
    topics: list[dict[str, object]],
    title: str = "Weighted Persona Convergence Map",
) -> go.Figure:
    """Build an interactive Plotly figure from already processed layout data."""

    fig = go.Figure()

    _add_persona_circles(fig, personas)
    _add_persona_hover_points(fig, personas, topics)
    _add_persona_labels(fig, personas)
    _add_topic_points(fig, personas, topics)
    _apply_layout(fig, personas, title)

    return fig


def _add_persona_circles(fig: go.Figure, personas: list[Persona]) -> None:
    for persona in personas:
        x, y = persona.position
        radius = persona.radius
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=x - radius,
            y0=y - radius,
            x1=x + radius,
            y1=y + radius,
            line={"color": persona.color, "width": 2},
            fillcolor=_hex_to_rgba(persona.color, 0.28),
            layer="below",
        )


def _add_persona_hover_points(
    fig: go.Figure,
    personas: list[Persona],
    topics: list[dict[str, object]],
) -> None:
    fig.add_trace(
        go.Scatter(
            x=[persona.position[0] for persona in personas],
            y=[persona.position[1] for persona in personas],
            mode="markers",
            marker={
                "size": [max(18, persona.radius * 18) for persona in personas],
                "color": "rgba(255,255,255,0.01)",
                "line": {"width": 0},
            },
            text=[build_persona_tooltip(persona, topics) for persona in personas],
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )


def _add_persona_labels(fig: go.Figure, personas: list[Persona]) -> None:
    label_positions = [persona_label_position(persona, personas) for persona in personas]
    fig.add_trace(
        go.Scatter(
            x=[point[0] for point in label_positions],
            y=[point[1] for point in label_positions],
            mode="text",
            text=[
                f"<b>{persona.name}</b><br>{persona.weight:.2f}%"
                for persona in personas
            ],
            textposition="middle center",
            textfont={"size": 13, "color": "#222222"},
            hoverinfo="skip",
            showlegend=False,
        )
    )


def _add_topic_points(
    fig: go.Figure,
    personas: list[Persona],
    topics: list[dict[str, object]],
) -> None:
    grouped_by_region: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    for topic in topics:
        grouped_by_region[tuple(topic["personas"])].append(topic)

    for topic_type, symbol, label in [
        ("Pain", "square", "Pain point"),
        ("Goal", "circle", "Goal"),
    ]:
        xs: list[float] = []
        ys: list[float] = []
        hover_texts: list[str] = []
        sizes: list[float] = []  # NEW: dynamic sizes based on representativity

        for persona_names, region_topics in grouped_by_region.items():
            for index, topic in enumerate(region_topics):
                if topic["type"] != topic_type:
                    continue
                x, y = topic_position(
                    list(persona_names),
                    personas,
                    index=index,
                    total=len(region_topics),
                )
                xs.append(x)
                ys.append(y)
                hover_texts.append(build_topic_tooltip(topic))
                
                # NEW: Scale marker size by representativity (0-100% -> 5-25px)
                representativity = topic.get("representativity", 50.0)
                marker_size = 5 + (representativity / 100.0) * 20
                sizes.append(marker_size)

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers",
                marker={
                    "size": sizes,  # CHANGED: now dynamic
                    "symbol": symbol,
                    "color": topic_color(topic_type),
                    "line": {"color": "white", "width": 1.5},
                },
                name=label,
                text=hover_texts,
                hovertemplate="%{text}<extra></extra>",
            )
        )


def _apply_layout(fig: go.Figure, personas: list[Persona], title: str) -> None:
    extent = max(
        abs(coord) + persona.radius + 1.8
        for persona in personas
        for coord in persona.position
    )
    fig.update_layout(
        title={"text": title, "x": 0.5},
        width=1200,
        height=800,
        autosize=True,
        hovermode="closest",
        dragmode="pan",
        legend={"orientation": "h", "x": 0.5, "xanchor": "center", "y": 1.02},
        margin={"l": 30, "r": 30, "t": 80, "b": 30},
        template="plotly_white",
    )
    fig.update_xaxes(
        range=[-extent, extent],
        visible=False,
        scaleanchor="y",
        scaleratio=1,
        constrain="domain",
    )
    fig.update_yaxes(
        range=[-extent, extent],
        visible=False,
        constrain="domain",
    )


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    color = hex_color.lstrip("#")
    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)
    return f"rgba({red},{green},{blue},{alpha})"
