from pathlib import Path

# Estrutura de diretórios do projeto
folders = [
    "data/raw",
    "data/processed",
    "data/outputs/diagrams",
    "data/outputs/tables",
    "data/outputs/reports",

    "src/models",
    "src/processing",
    "src/visualization",
    "src/utils",

    "notebooks",
    "tests"
]

# Arquivos base do projeto
files = {
    "requirements.txt": "",
    "README.md": "# Persona Framework\n",
    "main.py": "",

    "src/models/persona.py": "",
    "src/models/topic.py": "",
    "src/models/overlap.py": "",

    "src/processing/parser.py": "",
    "src/processing/overlap_calculator.py": "",
    "src/processing/impact_score.py": "",
    "src/processing/clustering.py": "",

    "src/visualization/venn_layout.py": "",
    "src/visualization/renderer.py": "",
    "src/visualization/labels.py": "",
    "src/visualization/export.py": "",

    "src/utils/colors.py": "",
    "src/utils/geometry.py": "",

    "tests/test_overlap.py": "",
    "tests/test_scores.py": "",
    "tests/test_geometry.py": "",

    "notebooks/exploratory_analysis.ipynb": ""
}

# Criação das pastas
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Criação dos arquivos
for filepath, content in files.items():
    file = Path(filepath)

    # Garante que a pasta pai existe
    file.parent.mkdir(parents=True, exist_ok=True)

    # Cria arquivo apenas se não existir
    if not file.exists():
        file.write_text(content, encoding="utf-8")

print("Estrutura do projeto criada com sucesso.")