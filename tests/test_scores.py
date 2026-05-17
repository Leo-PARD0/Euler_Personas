from src.models.overlap import Overlap
from src.models.topic import Topic, TopicType
from src.processing.impact_score import calculate_impact_scores


def test_calculate_impact_scores_uses_representativity():
    """Test that impact_score is derived from topic representativity.
    
    Topic-centric model: impact_score = representativity * overlap_level / 10
    """
    # Create topic with representativity 90%
    topic = Topic(
        name="Shared issue",
        type=TopicType.PAIN_POINT,
        personas=("A", "B", "C"),
        representativity=90.0,  # NEW: topic has observed representativity
        overlap_level=3
    )
    
    overlap = Overlap(
        personas=("A", "B", "C"),
        topics=[topic],
        accumulated_weight=60,  # No longer used for impact calculation
    )

    scores = calculate_impact_scores([overlap])

    # NEW: impact_score = 90.0 * 3 / 10 = 27.0
    assert abs(scores[0]["impact_score"] - 27.0) < 0.01
    assert scores[0]["overlap_level"] == 3
    assert scores[0]["representativity"] == 90.0  # NEW: representativity in output
