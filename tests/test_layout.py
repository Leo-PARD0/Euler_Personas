from src.models.persona import Persona
from src.utils.geometry import distance
from src.visualization.venn_layout import assign_weighted_circle_layout, persona_label_position, topic_position


def test_four_persona_intersection_topic_position_is_inside_all_circles():
    personas = [
        Persona("A", 100),
        Persona("B", 100),
        Persona("C", 100),
        Persona("D", 100),
    ]

    assign_weighted_circle_layout(personas)
    point = topic_position(["A", "B", "C", "D"], personas)

    assert all(distance(point, persona.position) <= persona.radius for persona in personas)


def test_layout_uses_absolute_weight_scale():
    personas = [Persona("A", 100), Persona("B", 25)]

    assign_weighted_circle_layout(personas)

    assert personas[0].radius > personas[1].radius


def test_single_persona_topic_position_stays_outside_other_circles_when_possible():
    personas = [
        Persona("A", 100),
        Persona("B", 100),
        Persona("C", 100),
        Persona("D", 100),
    ]

    assign_weighted_circle_layout(personas)
    point = topic_position(["A"], personas)
    included = personas[0]
    excluded = personas[1:]

    assert distance(point, included.position) <= included.radius
    assert all(distance(point, persona.position) > persona.radius for persona in excluded)


def test_three_persona_topic_position_avoids_four_way_intersection_when_possible():
    personas = [
        Persona("A", 100),
        Persona("B", 100),
        Persona("C", 100),
        Persona("D", 100),
    ]

    assign_weighted_circle_layout(personas)
    point = topic_position(["A", "B", "C"], personas)

    assert all(distance(point, persona.position) <= persona.radius for persona in personas[:3])
    assert distance(point, personas[3].position) > personas[3].radius


def test_persona_label_positions_are_on_outer_polygon():
    personas = [
        Persona("A", 100),
        Persona("B", 100),
        Persona("C", 100),
        Persona("D", 100),
    ]

    assign_weighted_circle_layout(personas)
    label_points = [persona_label_position(persona, personas) for persona in personas]

    assert len(set(label_points)) == 4
    assert all(distance(label, persona.position) > persona.radius for label, persona in zip(label_points, personas))
