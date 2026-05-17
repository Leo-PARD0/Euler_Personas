from src.models.persona import Persona
from src.processing.impact_score import calculate_impact_scores
from src.processing.overlap_calculator import calculate_overlaps
from src.models.topic import Topic, TopicType
from src.visualization.export_html import export_interactive_html
from src.visualization.renderer_plotly import render_interactive_persona_map
from src.visualization.support_page import load_support_routes
from src.visualization.venn_layout import assign_weighted_circle_layout


def test_plotly_renderer_reuses_persona_layout():
    personas = [Persona("A", 100), Persona("B", 80)]
    assign_weighted_circle_layout(personas)
    topics = [
        {
            "name": "Shared topic",
            "type": "Goal",
            "personas": ["A", "B"],
            "impact_score": 360,
        }
    ]

    fig = render_interactive_persona_map(personas, topics)

    assert len(fig.layout.shapes) == 2
    assert len(fig.data) >= 4
    assert fig.layout.xaxis.visible is False


def test_export_interactive_html_writes_standalone_file(tmp_path):
    personas = [Persona("A", 100), Persona("B", 80)]
    topics = [Topic("Shared topic", TopicType.GOAL, ("A", "B"))]
    assign_weighted_circle_layout(personas)
    scored_topics = calculate_impact_scores(calculate_overlaps(topics, personas))
    fig = render_interactive_persona_map(personas, scored_topics)
    output_path = tmp_path / "map.html"

    path = export_interactive_html(fig, output_path)

    content = path.read_text(encoding="utf-8")
    assert path.exists()
    assert "Plotly.newPlot" in content
    assert "Shared topic" in content
    assert 'href="#apoio"' in content
    assert '<section id="apoio"' in content
    assert 'src="https://cdn.plot.ly' not in content


def test_support_routes_load_donation_platforms(tmp_path):
    config_path = tmp_path / "donation_routes.json"
    config_path.write_text(
        """
        {
          "routes": [
            {
              "platform": "Ko-fi",
              "url": "https://ko-fi.com/example",
              "qr_image": "../../../assets/qrcode/kofi.png",
              "enabled": true
            },
            {
              "platform": "Disabled",
              "url": "https://example.com",
              "enabled": false
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    routes = load_support_routes(config_path)

    assert routes == [
        {
            "platform": "Ko-fi",
            "url": "https://ko-fi.com/example",
            "qr_image": "../../../assets/qrcode/kofi.png",
            "description": "",
        }
    ]
