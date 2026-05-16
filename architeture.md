persona-framework/
│
├── data/
│   ├── raw/
│   │   └── personas.csv
│   │
│   ├── processed/
│   │   └── intersections.json
│   │
│   └── outputs/
│       ├── diagrams/
│       ├── tables/
│       └── reports/
│
├── src/
│   ├── models/
│   │   ├── persona.py
│   │   ├── topic.py
│   │   └── overlap.py
│   │
│   ├── processing/
│   │   ├── parser.py
│   │   ├── overlap_calculator.py
│   │   ├── impact_score.py
│   │   └── clustering.py
│   │
│   ├── visualization/
│   │   ├── venn_layout.py
│   │   ├── renderer.py
│   │   ├── labels.py
│   │   └── export.py
│   │
│   └── utils/
│       ├── colors.py
│       └── geometry.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── tests/
│   ├── test_overlap.py
│   ├── test_scores.py
│   └── test_geometry.py
│
├── requirements.txt
├── pyproject.toml
├── README.md
└── main.py