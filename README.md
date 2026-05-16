# Weighted Persona Convergence Framework

Framework Python para transformar dados qualitativos de UX Research em mapas ponderados de convergencia entre personas.

## MVP

- Solicita ao usuario o caminho de um CSV unico de pesquisa.
- Valida existencia, tipo de arquivo e estrutura esperada.
- Infere personas a partir da coluna `Pessoa`.
- Inicia pesos iguais e permite ajustar a representatividade no preview.
- Calcula overlaps por conjunto de personas.
- Calcula `impact_score = sum(persona_weights) * overlap_frequency`.
- Abre preview interativo do diagrama ponderado.
- Mostra topicos apenas no hover dos marcadores.
- Permite ajustar pesos por slider ou input numerico com ate 2 casas decimais.
- Redistribui circulos e marcadores para manter os topicos nas interseccoes.
- Exporta PNG, SVG, HTML interativo, CSV e JSON apenas se o usuario escolher.

## Uso

```bash
.venv\Scripts\python.exe main.py
```

Fluxo:

```text
Enter research CSV path:
> C:\Users\LeoPardo\Downloads\Planilha sem titulo.csv

[preview opens]

Adjust persona weights with the sliders.
Or type exact values in the numeric fields beside each slider.
Hover topic markers to inspect pain points and goals.

Click `Export`, deselect any formats you do not want, then click `Save`.
```

Saidas opcionais:

- `data/outputs/diagrams/weighted_persona_map.png`
- `data/outputs/diagrams/weighted_persona_map.svg`
- `data/outputs/diagrams/weighted_persona_map.html`
- `data/outputs/tables/topic_priorities.csv`
- `data/processed/overlaps.json`

## Arquitetura

- `main.py`: orquestracao e interacao com o usuario.
- `src/visualization/renderer.py`: constroi e retorna a figura Matplotlib.
- `src/visualization/renderer_plotly.py`: constroi a visualizacao HTML interativa.
- `src/visualization/export.py`: salva figuras, tabelas e JSON.
- `src/visualization/export_html.py`: salva HTML standalone com Plotly inline.
- `src/visualization/tooltip_builder.py`: centraliza textos de hover.

O HTML exportado e standalone: o JavaScript do Plotly fica embutido no arquivo,
sem dependencia de CDN, internet ou arquivos locais do projeto.

## Formato dos dados

CSV unico:

```csv
Elemento,Tipo,Pessoa
Infraestrutura precaria,Pain Point,"Marcelo Santos, Lucas Ferreira"
Garantir quorum,Objetivo,"Marcelo Santos, Gabriela Ferreira"
```

Tipos aceitos:

- `Pain Point`, `Pain`, `Dor`
- `Objetivo`, `Goal`
