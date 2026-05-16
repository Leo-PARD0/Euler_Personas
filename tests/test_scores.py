from src.models.overlap import Overlap
from src.models.topic import Topic, TopicType
from src.processing.impact_score import calculate_impact_scores


def test_calculate_impact_scores_uses_weight_times_overlap_frequency():
    overlap = Overlap(
        personas=("A", "B", "C"),
        topics=[Topic("Shared issue", TopicType.PAIN_POINT, ("A", "B", "C"))],
        accumulated_weight=60,
    )

    scores = calculate_impact_scores([overlap])

    assert scores[0]["impact_score"] == 180
    assert scores[0]["overlap_level"] == 3
