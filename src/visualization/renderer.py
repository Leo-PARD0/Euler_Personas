from __future__ import annotations

from collections import defaultdict
from textwrap import fill

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.widgets import Button, CheckButtons, Slider, TextBox

from src.models.persona import Persona
from src.utils.colors import topic_color
from src.visualization.venn_layout import assign_weighted_circle_layout, persona_label_position, topic_position


def render_weighted_persona_map(
    personas: list[Persona],
    topics: list[dict[str, object]],
    title: str = "Weighted Persona Convergence Map",
    interactive_controls: bool = True,
    export_callback=None,
) -> Figure:
    """Build the weighted persona map figure without saving it."""

    assign_weighted_circle_layout(personas)

    bottom_margin = 0.12 + min(len(personas), 8) * 0.045 if interactive_controls else 0.08
    fig, ax = plt.subplots(figsize=(13, 9))
    fig.subplots_adjust(bottom=bottom_margin)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=18, weight="bold", pad=18)

    persona_circles: dict[str, Circle] = {}
    persona_labels = {}

    for persona in personas:
        circle = Circle(
            persona.position,
            persona.radius,
            color=persona.color,
            alpha=0.28,
            linewidth=2,
            ec=persona.color,
        )
        ax.add_patch(circle)
        persona_circles[persona.name] = circle
        label_position = persona_label_position(persona, personas)
        persona_labels[persona.name] = ax.text(
            label_position[0],
            label_position[1],
            f"{persona.name}\n{persona.weight:.2f}%",
            ha="center",
            va="center",
            fontsize=11,
            weight="bold",
            color="#222222",
        )

    topic_artists = _draw_topic_markers(ax, personas, topics)
    annotation = _build_hover_annotation(ax)

    def redraw_layout() -> None:
        assign_weighted_circle_layout(personas)

        for persona in personas:
            circle = persona_circles[persona.name]
            circle.center = persona.position
            circle.radius = persona.radius
            label = persona_labels[persona.name]
            label.set_position(persona_label_position(persona, personas))
            label.set_text(f"{persona.name}\n{persona.weight:.2f}%")

        _update_topic_positions(topic_artists, personas)
        _update_bounds(ax, personas)
        fig.canvas.draw_idle()

    _update_bounds(ax, personas)
    _build_legend(ax)
    _connect_hover(fig, ax, topic_artists, annotation)

    if interactive_controls:
        _build_weight_sliders(fig, personas, redraw_layout)
        if export_callback is not None:
            _build_export_panel(fig, export_callback)

    return fig


def _draw_topic_markers(ax, personas: list[Persona], topics: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped_by_region: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    for topic in topics:
        grouped_by_region[tuple(topic["personas"])].append(topic)

    topic_artists: list[dict[str, object]] = []
    for persona_names, region_topics in grouped_by_region.items():
        for index, topic in enumerate(region_topics):
            x, y = topic_position(
                list(persona_names),
                personas,
                index=index,
                total=len(region_topics),
            )
            marker = "o" if topic["type"] == "Goal" else "s"
            artist = ax.scatter(
                [x],
                [y],
                s=95,
                marker=marker,
                color=topic_color(str(topic["type"])),
                edgecolor="white",
                linewidth=1.3,
                zorder=4,
            )
            topic_artists.append(
                {
                    "artist": artist,
                    "topic": topic,
                    "index": index,
                    "total": len(region_topics),
                    "personas": list(persona_names),
                }
            )

    return topic_artists


def _update_topic_positions(topic_artists: list[dict[str, object]], personas: list[Persona]) -> None:
    for item in topic_artists:
        x, y = topic_position(
            item["personas"],
            personas,
            index=item["index"],
            total=item["total"],
        )
        item["artist"].set_offsets([[x, y]])


def _build_hover_annotation(ax):
    annotation = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(14, 14),
        textcoords="offset points",
        bbox={"boxstyle": "round,pad=0.35", "fc": "white", "ec": "#bbbbbb", "alpha": 0.96},
        arrowprops={"arrowstyle": "->", "color": "#666666"},
        fontsize=9,
        zorder=10,
    )
    annotation.set_visible(False)
    return annotation


def _connect_hover(fig: Figure, ax, topic_artists: list[dict[str, object]], annotation) -> None:
    def on_move(event) -> None:
        if event.inaxes != ax:
            if annotation.get_visible():
                annotation.set_visible(False)
                fig.canvas.draw_idle()
            return

        for item in topic_artists:
            contains, _ = item["artist"].contains(event)
            if contains:
                topic = item["topic"]
                x, y = item["artist"].get_offsets()[0]
                annotation.xy = (x, y)
                annotation.set_text(
                    "\n".join(
                        [
                            fill(str(topic["name"]), width=58),
                            f"Type: {topic['type']}",
                            f"Personas: {', '.join(topic['personas'])}",
                            f"Impact score: {topic['impact_score']:.2f}",
                        ]
                    )
                )
                annotation.set_visible(True)
                fig.canvas.draw_idle()
                return

        if annotation.get_visible():
            annotation.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_move)


def _build_weight_sliders(fig: Figure, personas: list[Persona], on_change) -> None:
    slider_height = 0.025
    slider_gap = 0.012
    start_y = 0.035
    max_sliders = min(len(personas), 8)

    for index, persona in enumerate(personas[:max_sliders]):
        y = start_y + index * (slider_height + slider_gap)
        slider_axis = fig.add_axes([0.22, y, 0.46, slider_height])
        slider = Slider(
            ax=slider_axis,
            label=persona.name,
            valmin=1,
            valmax=100,
            valinit=persona.weight,
            valfmt="%.2f",
        )
        input_axis = fig.add_axes([0.72, y, 0.08, slider_height])
        text_box = TextBox(input_axis, "", initial=f"{persona.weight:.2f}")
        syncing = {"active": False}

        def apply_weight(
            value: float,
            current_persona=persona,
            current_text_box=text_box,
            state=syncing,
        ) -> None:
            weight = round(max(1.0, min(100.0, float(value))), 2)
            current_persona.weight = weight
            if not state["active"]:
                state["active"] = True
                current_text_box.set_val(f"{weight:.2f}")
                state["active"] = False
            on_change()

        def update_from_slider(value, state=syncing, apply=apply_weight) -> None:
            if state["active"]:
                return
            apply(float(value))

        def update_from_text(
            value,
            current_persona=persona,
            current_slider=slider,
            current_text_box=text_box,
            state=syncing,
            apply=apply_weight,
        ) -> None:
            if state["active"]:
                return
            try:
                weight = round(float(value.replace(",", ".")), 2)
            except ValueError:
                state["active"] = True
                current_text_box.set_val(f"{current_persona.weight:.2f}")
                state["active"] = False
                return

            weight = max(1.0, min(100.0, weight))
            state["active"] = True
            current_slider.set_val(weight)
            state["active"] = False
            apply(weight)

        slider.on_changed(update_from_slider)
        text_box.on_submit(update_from_text)
        if not hasattr(fig, "_persona_weight_sliders"):
            fig._persona_weight_sliders = []
        if not hasattr(fig, "_persona_weight_inputs"):
            fig._persona_weight_inputs = []
        fig._persona_weight_sliders.append(slider)
        fig._persona_weight_inputs.append(text_box)


def _build_export_panel(fig: Figure, export_callback) -> None:
    export_button_axis = fig.add_axes([0.84, 0.035, 0.1, 0.035])
    export_button = Button(export_button_axis, "Export")

    check_axis = fig.add_axes([0.82, 0.09, 0.14, 0.17])
    labels = ["PNG", "SVG", "HTML", "CSV", "JSON"]
    checks = CheckButtons(check_axis, labels, [True] * len(labels))
    confirm_axis = fig.add_axes([0.845, 0.275, 0.09, 0.032])
    confirm_button = Button(confirm_axis, "Save")
    status_text = fig.text(0.82, 0.315, "", fontsize=8, color="#2E7D5B")

    panel_axes = [check_axis, confirm_axis]
    for axis in panel_axes:
        axis.set_visible(False)

    def set_panel_visible(visible: bool) -> None:
        for axis in panel_axes:
            axis.set_visible(visible)
        status_text.set_visible(visible)
        fig.canvas.draw_idle()

    def toggle_panel(_event) -> None:
        set_panel_visible(not check_axis.get_visible())

    def save_selected(_event) -> None:
        selected_formats = [
            label.lower()
            for label, active in zip(labels, checks.get_status())
            if active
        ]
        if not selected_formats:
            status_text.set_text("Select at least one format.")
            fig.canvas.draw_idle()
            return

        exported_paths = export_callback(selected_formats)
        status_text.set_text(f"Exported {len(exported_paths)} file(s).")
        fig.canvas.draw_idle()

    export_button.on_clicked(toggle_panel)
    confirm_button.on_clicked(save_selected)

    fig._export_button = export_button
    fig._export_checks = checks
    fig._export_confirm_button = confirm_button


def _build_legend(ax) -> None:
    legend_handles = [
        plt.Line2D([0], [0], marker="s", color="w", label="Pain point", markerfacecolor=topic_color("Pain"), markersize=9),
        plt.Line2D([0], [0], marker="o", color="w", label="Goal", markerfacecolor=topic_color("Goal"), markersize=9),
    ]
    ax.legend(handles=legend_handles, loc="upper right", frameon=False)


def _update_bounds(ax, personas: list[Persona]) -> None:
    max_extent = max(
        abs(coord) + persona.radius + 1.8
        for persona in personas
        for coord in persona.position
    )
    ax.set_xlim(-max_extent, max_extent)
    ax.set_ylim(-max_extent, max_extent)
