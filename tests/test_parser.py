from src.models.topic import TopicType
from src.processing.parser import load_research_csv


def test_load_research_csv_with_portuguese_columns(tmp_path):
    csv_path = tmp_path / "research.csv"
    csv_path.write_text(
        "Elemento,Tipo,Pessoa\n"
        "Infraestrutura,Pain Point,\"Marcelo Santos, Lucas Ferreira\"\n"
        "Garantir quorum,Objetivo,\"Lucas Ferreira, Natacha Silva\"\n",
        encoding="utf-8",
    )

    personas, topics = load_research_csv(csv_path)

    assert [persona.name for persona in personas] == [
        "Lucas Ferreira",
        "Marcelo Santos",
        "Natacha Silva",
    ]
    assert [persona.weight for persona in personas] == [100.0, 100.0, 100.0]
    assert topics[0].name == "Infraestrutura"
    assert topics[0].type == TopicType.PAIN_POINT
    assert topics[0].personas == ("Marcelo Santos", "Lucas Ferreira")
    assert topics[1].type == TopicType.GOAL
