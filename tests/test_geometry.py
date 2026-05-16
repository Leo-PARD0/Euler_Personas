from src.utils.geometry import circles_overlap, distance, weighted_radius


def test_distance():
    assert distance((0, 0), (3, 4)) == 5


def test_circles_overlap():
    assert circles_overlap((0, 0), 2, (3, 0), 2)
    assert not circles_overlap((0, 0), 1, (3, 0), 1)


def test_weighted_radius_increases_with_weight():
    assert weighted_radius(90, 100) > weighted_radius(20, 100)
