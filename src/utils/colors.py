PERSONA_PALETTE = [
    "#4E79A7",
    "#F28E2B",
    "#59A14F",
    "#E15759",
    "#76B7B2",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
]

TOPIC_TYPE_COLORS = {
    "Pain": "#C44536",
    "Goal": "#2E7D5B",
}


def persona_color(index: int) -> str:
    return PERSONA_PALETTE[index % len(PERSONA_PALETTE)]


def topic_color(topic_type: str) -> str:
    return TOPIC_TYPE_COLORS.get(topic_type, "#333333")
