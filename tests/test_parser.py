from src.models.topic import TopicType
from src.processing.parser import load_research_csv


def test_load_research_csv_with_portuguese_columns(tmp_path):
    """Test loading CSV with Portuguese column names and representativity.
    
    With topic-centric model, personas get weight derived from their topics' representativity.
    CSV without representativity column will result in personas with 0 weight (no data).
    """
    csv_path = tmp_path / "research.csv"
    csv_path.write_text(
        "Elemento,Tipo,Pessoa,Representatividade (%)\n"
        "Infraestrutura,Pain Point,\"Marcelo Santos, Lucas Ferreira\",90.5\n"
        "Garantir quorum,Objetivo,\"Lucas Ferreira, Natacha Silva\",85.0\n",
        encoding="utf-8",
    )

    personas, topics = load_research_csv(csv_path)

    assert [persona.name for persona in personas] == [
        "Lucas Ferreira",
        "Marcelo Santos",
        "Natacha Silva",
    ]
    
    # Derived weights: Lucas = avg(90.5, 85.0) = 87.75, Marcelo = 90.5, Natacha = 85.0
    persona_weights = {p.name: p.weight for p in personas}
    assert abs(persona_weights["Lucas Ferreira"] - 87.75) < 0.01
    assert abs(persona_weights["Marcelo Santos"] - 90.5) < 0.01
    assert abs(persona_weights["Natacha Silva"] - 85.0) < 0.01
    
    assert topics[0].name == "Infraestrutura"
    assert topics[0].type == TopicType.PAIN_POINT
    assert topics[0].personas == ("Marcelo Santos", "Lucas Ferreira")
    assert topics[0].representativity == 90.5  # NEW: check representativity
    assert topics[1].type == TopicType.GOAL
    assert topics[1].representativity == 85.0  # NEW: check representativity
