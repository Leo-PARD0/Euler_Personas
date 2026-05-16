from src.models.persona import Persona
from src.models.topic import Topic, TopicType
from src.processing.overlap_calculator import calculate_overlaps


def test_calculate_overlaps_groups_same_persona_set():
    personas = [Persona("A", 10), Persona("B", 20)]
    topics = [
        Topic("Topic 1", TopicType.PAIN_POINT, ("A", "B"), 2),
        Topic("Topic 2", TopicType.GOAL, ("B", "A"), 2),
    ]

    overlaps = calculate_overlaps(topics, personas)

    assert len(overlaps) == 1
    assert overlaps[0].personas == ("A", "B")
    assert overlaps[0].accumulated_weight == 30
    assert overlaps[0].topic_names == ["Topic 1", "Topic 2"]
