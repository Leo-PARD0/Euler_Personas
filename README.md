# Euler Personas - Framework de Convergência Ponderada entre Personas

Euler Personas é um framework em Python para UX Research e Product Research. Ele transforma achados qualitativos em um mapa quantitativo de convergência entre personas, dores e objetivos, ajudando times a priorizar tópicos que combinam incidência observada e presença em múltiplos contextos de uso.

## Apoie o Projeto

Se este projeto foi útil para você, considere apoiar o desenvolvimento do framework.

<div align="center">

<a href="https://livepix.gg/leo1pardo" target="_blank">

<img src="./assets/qrcode/Livepix.png" 
     alt="Apoie via LivePIX" 
     width="220"/>

</a>

<br>

[💜 Apoiar via LivePIX](https://livepix.gg/leo1pardo)

</div>


## Antes de Executar

Antes de rodar o framework, você precisa:

1. Gerar ou preparar um CSV compatível.
2. Revisar manualmente os tópicos, personas e percentuais.
3. Instalar as dependências do projeto.
4. Executar `python main.py`.

O framework não interpreta entrevistas brutas diretamente. Ele visualiza uma síntese já organizada em CSV.

## Prompt do NotebookLM

O NotebookLM pode apoiar a síntese do CSV a partir de materiais como personas, entrevistas, pesquisas quantitativas, benchmarks e sínteses de discovery. Ele não substitui validação humana.

### Prompt Base

```text
Você receberá como contexto:

- documentação de personas;
- pesquisas qualitativas;
- pesquisas quantitativas;
- análises de benchmarking;
- entrevistas;
- sínteses de discovery;
- evidências e achados de UX Research.

Sua tarefa é cruzar essas informações para identificar:

- dores recorrentes;
- objetivos recorrentes;
- necessidades compartilhadas;
- padrões de comportamento;
- convergências entre personas.

Gere uma tabela CSV com os campos:

Elemento,Tipo,Pessoa,Representatividade (%),Origem do Dado

Regras:

1. Elemento
- Deve representar uma dor, objetivo ou achado consolidado.
- Agrupe tópicos semanticamente semelhantes.
- Evite duplicações.

2. Tipo
Use apenas:
- Pain Point
- Goal

3. Pessoa
- Liste todas as personas relacionadas ao elemento.
- Separe múltiplas personas por vírgula ou ponto e vírgula.

4. Representatividade (%)
- Use dados quantitativos quando existirem.
- Quando não houver porcentagem explícita, estime com base na recorrência observada.
- Use formato percentual.

5. Origem do Dado
- Explique brevemente a origem do achado.
- Cite recorrência observada, benchmark, entrevistas ou padrões identificados.

Objetivo final:
Gerar uma tabela consolidada de convergências entre personas, dores e objetivos para alimentar um framework de visualização e priorização de UX Research.
```

### Validação Humana

Depois de gerar o CSV, revise:

- se os elementos estão agrupados sem perder significado;
- se não há tópicos duplicados;
- se as personas relacionadas fazem sentido;
- se a representatividade é defensável;
- se a origem do dado preserva rastreabilidade.

## Como o CSV Foi Gerado

> Placeholder para explicação metodológica da geração do CSV.

Adicionar manualmente:
- origem da pesquisa;
- quantidade de entrevistas;
- metodologia utilizada;
- critérios de agrupamento;
- cálculo da representatividade;
- fluxo de síntese via NotebookLM;
- validação humana dos tópicos.

## Estrutura do CSV

O framework espera um único CSV. A estrutura recomendada é:

```csv
Elemento,Tipo,Pessoa,Representatividade (%),Origem do Dado
Infraestrutura precária,Pain,"Marcelo;Lucas;Natacha",90.3,"28 dos 31 respondentes relataram problemas estruturais"
Garantir quórum,Goal,"Marcelo;Lucas;Gabriela",83.1,"Objetivo recorrente em entrevistas e benchmarking"
```

Campos aceitos:

| Campo canônico | Obrigatório | Cabeçalhos aceitos |
|---|---:|---|
| `topic` | sim | `topic`, `topico`, `tópico`, `elemento`, `dor`, `objetivo` |
| `type` | sim | `type`, `tipo`, `categoria` |
| `personas` | sim | `personas`, `pessoa`, `pessoas` |
| `weight` | não | `weight`, `peso`, `representatividade`, `representatividade (%)` |
| `evidence` | não | `evidence`, `origem`, `origem do dado`, `fonte` |

### Regras de Formato

- Use UTF-8.
- Use vírgula como separador padrão.
- Use aspas em células que contêm vírgulas.
- Use uma linha por tópico.
- Separe múltiplas personas por `;` ou `,`. O `;` é mais seguro porque a vírgula também separa colunas.

Tipos aceitos:

- Dores: `Pain`, `Pain Point`, `PainPoint`, `Dor`, `Dores`
- Objetivos: `Goal`, `Objetivo`, `Objetivos`

Representatividade aceita:

```text
90.3
90.30
90,30
90.30%
90,30%
```

A representatividade é limitada internamente ao intervalo de `0` a `100`. Se a coluna não existir, os tópicos recebem `0.0`.

## Descrição Geral

O framework:

- extrai tópicos do CSV;
- classifica tópicos como dores ou objetivos;
- infere personas a partir da relação tópico-persona;
- deriva pesos de personas pela média de representatividade dos tópicos relacionados;
- agrupa tópicos por conjunto de personas;
- calcula impacto por tópico;
- abre um dashboard de pré-visualização;
- exporta PNG, SVG, HTML, CSV e JSON quando solicitado.

Ele foi criado para apoiar perguntas como:

- Quais dores afetam mais de uma persona?
- Quais objetivos aparecem em contextos diferentes?
- Quais tópicos combinam alta incidência e alta convergência?
- Quais achados devem orientar priorização de produto?

## Conceitos Fundamentais

### Visualização Centrada em Personas

As personas organizam o espaço visual. Cada persona aparece como um círculo, e os tópicos são posicionados dentro de círculos ou em interseções conforme as personas relacionadas.

Na implementação atual:

- o raio da persona é proporcional ao seu peso;
- o peso é derivado da média de representatividade dos tópicos associados;
- os círculos usam um layout radial;
- rótulos ficam fora dos círculos.

### Análise Centrada em Tópicos

Os tópicos são a unidade analítica principal. Um tópico possui nome, tipo, personas relacionadas, representatividade, nível de overlap, score de impacto e evidência opcional.

Assim, o modelo é topic-centric na análise e persona-centric na visualização.

## Instalação e Execução

Instale as dependências:

```bash
pip install -r requirements.txt
```

No Windows, usando o ambiente virtual do projeto:

```bash
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Execute:

```bash
python main.py
```

Informe o caminho do CSV quando solicitado:

```text
Enter research CSV path:
> C:\path\to\research.csv
```

## Fluxo de Execução

```text
Instalar dependências
-> Preparar CSV
-> Executar main.py
-> Parsing
-> Processamento dos tópicos
-> Extração de personas
-> Cálculo de overlaps
-> Cálculo de impacto
-> Layout
-> Dashboard de pré-visualização
-> Exportação opcional
```

No dashboard, o usuário pode ajustar pesos, inspecionar tópicos por hover, abrir a aba de apoio e exportar os formatos selecionados.

## Cálculos

### Representatividade da Persona

```text
persona.weight = média(representatividade dos tópicos ligados à persona)
```

Exemplo:

```text
Tópico A -> Marcelo, representatividade 90
Tópico B -> Marcelo, representatividade 70

Peso de Marcelo = (90 + 70) / 2 = 80
```

### Impact Score

Fórmula atual em `src/processing/impact_score.py`:

```text
impact_score = topic.representativity * (overlap_level / 10.0)
```

Exemplo:

```text
representatividade = 90.0
overlap_level = 3
impact_score = 27.0
```

`Overlap.accumulated_weight` é calculado como soma dos pesos das personas envolvidas, mas não entra na fórmula atual de impacto.

## Visualização

### Preview no Dashboard

O preview é construído com Matplotlib e inclui:

- círculos de personas;
- marcadores de tópicos;
- hover nos tópicos;
- sliders e campos numéricos de peso;
- painel de exportação;
- abas `Mapa` e `Apoio`.

No preview, dores usam quadrados e objetivos usam círculos. O tamanho dos marcadores é fixo.

### HTML Exportado

O HTML usa Plotly e inclui:

- página `Mapa`;
- Página de Apoio;
- JavaScript do Plotly embutido;
- pan, zoom e hover;
- marcador com tamanho dinâmico por representatividade.

No HTML:

```text
marker_size = 5 + (representativity / 100.0) * 20
```

## Página de Apoio

A Página de Apoio serve para financiamento do projeto, doações e links para plataformas onde pessoas podem apoiar o desenvolvimento.

Ela aparece:

- na aba de apoio do dashboard;
- no HTML exportado.

Rotas de apoio:

```text
config/support/donation_routes.json
```

QR codes:

```text
assets/qrcode/
```

Formato atual:

```json
{
  "routes": [
    {
      "platform": "LivePIX",
      "url": "https://example.com",
      "qr_image": "../../../assets/qrcode/example.png",
      "description": "Descrição opcional",
      "enabled": true
    }
  ]
}
```

O arquivo ainda se chama `donation_routes.json` por compatibilidade, mas a terminologia do projeto é rotas de apoio.

## Outputs

As exportações são opcionais:

```text
data/outputs/diagrams/weighted_persona_map.png
data/outputs/diagrams/weighted_persona_map.svg
data/outputs/diagrams/weighted_persona_map.html
data/outputs/tables/topic_priorities.csv
data/processed/overlaps.json
```

`topic_priorities.csv` usa:

```text
name,type,personas,overlap_level,accumulated_weight,impact_score,centrality
```

Comportamento atual: `name`, `type`, `personas`, `overlap_level` e `impact_score` são preenchidos. `accumulated_weight` e `centrality` existem no schema, mas ainda não são preenchidos no export atual.

`overlaps.json` contém grupos de overlap com personas, tópicos, impacto, peso acumulado e centralidade. Atualmente não inclui `representativity` nem `evidence`.

## Arquitetura

```text
Euler_Personas/
|-- assets/qrcode/
|-- config/support/donation_routes.json
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- outputs/
|-- notebooks/
|-- src/
|   |-- models/
|   |-- processing/
|   |-- utils/
|   `-- visualization/
|-- tests/
|-- main.py
|-- requirements.txt
`-- README.md
```

Módulos principais:

- `main.py`: orquestra execução, preview e exportação.
- `src/models/`: define `Persona`, `Topic` e `Overlap`.
- `src/processing/parser.py`: lê e normaliza o CSV.
- `src/processing/overlap_calculator.py`: agrupa tópicos por personas.
- `src/processing/impact_score.py`: calcula impacto.
- `src/visualization/renderer.py`: dashboard Matplotlib.
- `src/visualization/renderer_plotly.py`: visualização HTML.
- `src/visualization/export.py`: PNG, SVG, CSV e JSON.
- `src/visualization/export_html.py`: HTML standalone.
- `src/visualization/support_page.py`: Página de Apoio.

## Interpretação dos Resultados

- Círculos maiores indicam personas com maior peso derivado ou ajustado.
- Overlaps indicam tópicos compartilhados por múltiplas personas.
- Quadrados representam dores.
- Círculos representam objetivos.
- Score alto indica alta representatividade e presença em mais personas.
- Evidência no CSV ajuda a preservar rastreabilidade metodológica.

O resultado deve ser lido como artefato de apoio à decisão, não como decisão automática.

## Testes

```bash
python -m pytest
```

A suíte cobre parsing, geometria, layout, overlaps, score, renderer Matplotlib e exportação HTML.

## Estado Atual

Implementado:

- CSV único;
- parser topic-centric;
- pesos derivados de personas;
- agrupamento por conjunto de personas;
- score baseado em representatividade;
- preview Matplotlib;
- exportação PNG, SVG, HTML, CSV e JSON;
- Página de Apoio no preview e no HTML.

Limitações atuais:

- tamanho de marcador dinâmico existe no HTML, mas não no preview;
- `accumulated_weight` e `centrality` não são preenchidos no CSV exportado;
- `overlaps.json` ainda não inclui `representativity` nem `evidence`;
- apenas as primeiras 8 personas recebem sliders visíveis;
- não há integração automatizada com NotebookLM.

## Roadmap

- preencher todos os campos do CSV exportado;
- incluir representatividade e evidência no JSON;
- alinhar marcadores do preview com o HTML;
- adicionar validação formal de schema;
- adicionar datasets de exemplo;
- validar empiricamente o prompt NotebookLM;
- gerar relatórios em `data/outputs/reports/`;
- adicionar execução não interativa;
- permitir fórmulas de score configuráveis.

## Fundamentação Conceitual

Euler Personas parte de três movimentos:

1. Achados qualitativos viram tópicos estruturados.
2. Convergências entre personas são representadas espacialmente.
3. Priorização combina incidência observada e amplitude de overlap.

O framework organiza evidências, explicita critérios e torna comparável uma síntese de UX/Product Research.
