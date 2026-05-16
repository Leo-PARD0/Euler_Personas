from matplotlib.figure import Figure

from src.models.persona import Persona
from src.visualization.renderer import render_weighted_persona_map


def test_renderer_returns_figure_without_exporting():
    personas = [Persona("A", 10), Persona("B", 20)]
    topics = [
        {
            "name": "Shared topic",
            "type": "Goal",
            "personas": ["A", "B"],
            "impact_score": 60,
        }
    ]

    fig = render_weighted_persona_map(personas, topics)

    assert isinstance(fig, Figure)


def test_renderer_adds_weight_sliders_for_interactive_preview():
    personas = [Persona("A", 100), Persona("B", 100)]
    topics = [
        {
            "name": "Shared topic",
            "type": "Goal",
            "personas": ["A", "B"],
            "impact_score": 200,
        }
    ]

    fig = render_weighted_persona_map(personas, topics)
    fig._persona_weight_sliders[1].set_val(40)

    assert personas[1].weight == 40


def test_renderer_weight_text_input_accepts_float():
    personas = [Persona("A", 100), Persona("B", 100)]
    topics = [
        {
            "name": "Shared topic",
            "type": "Goal",
            "personas": ["A", "B"],
            "impact_score": 200,
        }
    ]

    fig = render_weighted_persona_map(personas, topics)
    fig._persona_weight_inputs[1].set_val("42.37")

    assert personas[1].weight == 42.37


def test_renderer_weight_controls_update_their_own_persona():
    personas = [
        Persona("A", 100),
        Persona("B", 100),
        Persona("C", 100),
        Persona("D", 100),
    ]
    topics = [
        {
            "name": "Shared topic",
            "type": "Goal",
            "personas": ["A", "B", "C", "D"],
            "impact_score": 400,
        }
    ]

    fig = render_weighted_persona_map(personas, topics)
    fig._persona_weight_sliders[0].set_val(10)
    fig._persona_weight_sliders[1].set_val(20)
    fig._persona_weight_inputs[2].set_val("30.50")
    fig._persona_weight_inputs[3].set_val("40.25")

    assert [persona.weight for persona in personas] == [10, 20, 30.5, 40.25]


def test_renderer_adds_export_panel_when_callback_is_provided():
    personas = [Persona("A", 100), Persona("B", 100)]
    topics = [
        {
            "name": "Shared topic",
            "type": "Goal",
            "personas": ["A", "B"],
            "impact_score": 200,
        }
    ]

    fig = render_weighted_persona_map(
        personas,
        topics,
        export_callback=lambda selected_formats: selected_formats,
    )

    assert hasattr(fig, "_export_button")
    assert hasattr(fig, "_export_checks")
    assert hasattr(fig, "_export_confirm_button")
