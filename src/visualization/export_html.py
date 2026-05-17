from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go

from src.visualization.export import ensure_parent_dir
from src.visualization.support_page import load_support_routes, render_support_cards


def export_interactive_html(fig: go.Figure, output_path: str | Path) -> Path:
    path = ensure_parent_dir(output_path)
    plot_markup = fig.to_html(
        include_plotlyjs=True,
        full_html=False,
        config={
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": True,
            "toImageButtonOptions": {"format": "png", "scale": 2},
        },
    )
    support_markup = render_support_cards(load_support_routes())

    path.write_text(
        _build_preview_shell(plot_markup=plot_markup, support_markup=support_markup),
        encoding="utf-8",
    )
    return path


def _build_preview_shell(plot_markup: str, support_markup: str) -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Euler Personas - Resultado</title>
    <style>
        :root {{
            color-scheme: light;
            --bg: #f5f7fb;
            --panel: #ffffff;
            --text: #1f2937;
            --muted: #667085;
            --line: #d9e1ec;
            --accent: #146c94;
            --accent-strong: #0f4f6e;
            --shadow: 0 12px 34px rgba(16, 24, 40, 0.08);
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            min-height: 100vh;
            background: var(--bg);
            color: var(--text);
            font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        }}

        .app-header {{
            position: sticky;
            top: 0;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 12px 22px;
            border-bottom: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(12px);
        }}

        .brand {{
            min-width: 0;
            font-size: 15px;
            font-weight: 700;
            white-space: nowrap;
        }}

        .nav {{
            display: inline-flex;
            gap: 4px;
            padding: 4px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #eef3f8;
        }}

        .nav a {{
            min-width: 92px;
            padding: 8px 12px;
            border-radius: 6px;
            color: var(--muted);
            font-size: 14px;
            font-weight: 650;
            text-align: center;
            text-decoration: none;
        }}

        .nav a[aria-current="page"] {{
            background: var(--panel);
            color: var(--accent-strong);
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.08);
        }}

        main {{
            width: min(1280px, 100%);
            margin: 0 auto;
            padding: 18px;
        }}

        .page {{
            display: none;
        }}

        .page.is-active {{
            display: block;
        }}

        .page.support-page.is-active {{
            display: grid;
        }}

        .plot-panel {{
            min-height: calc(100vh - 96px);
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            box-shadow: var(--shadow);
            overflow: hidden;
        }}

        .plot-panel .plotly-graph-div {{
            width: 100% !important;
            min-height: calc(100vh - 118px);
        }}

        .support-page {{
            display: grid;
            gap: 14px;
            max-width: 920px;
            margin: 0 auto;
            padding: 18px 0 42px;
        }}

        .support-intro {{
            padding: 2px 2px 8px;
        }}

        .support-intro h1 {{
            margin: 0 0 6px;
            font-size: clamp(28px, 5vw, 44px);
            line-height: 1.05;
            letter-spacing: 0;
        }}

        .support-intro p,
        .support-card p,
        .support-empty p {{
            margin: 0;
            color: var(--muted);
            line-height: 1.55;
        }}

        .support-card,
        .support-empty {{
            display: grid;
            grid-template-columns: 132px 1fr;
            gap: 18px;
            align-items: center;
            padding: 18px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            box-shadow: var(--shadow);
        }}

        .support-empty {{
            grid-template-columns: 1fr;
        }}

        .support-card h2,
        .support-empty h2 {{
            margin: 0 0 6px;
            font-size: 20px;
            letter-spacing: 0;
        }}

        .support-qr {{
            width: 132px;
            height: 132px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            object-fit: contain;
        }}

        .support-qr-placeholder {{
            display: grid;
            place-items: center;
            color: var(--muted);
            font-weight: 800;
        }}

        .support-link {{
            display: inline-flex;
            align-items: center;
            min-height: 38px;
            margin-top: 14px;
            padding: 8px 12px;
            border-radius: 6px;
            background: var(--accent);
            color: #ffffff;
            font-weight: 700;
            text-decoration: none;
        }}

        .support-link:hover {{
            background: var(--accent-strong);
        }}

        .support-muted {{
            display: inline-block;
            margin-top: 14px;
            color: var(--muted);
            font-size: 14px;
        }}

        code {{
            padding: 2px 5px;
            border-radius: 5px;
            background: #eef3f8;
            color: #344054;
            font-size: 0.92em;
        }}

        @media (max-width: 680px) {{
            .app-header {{
                align-items: stretch;
                flex-direction: column;
                padding: 10px 12px;
            }}

            .nav {{
                width: 100%;
            }}

            .nav a {{
                flex: 1;
                min-width: 0;
            }}

            main {{
                padding: 12px;
            }}

            .support-card {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header class="app-header">
        <div class="brand">Euler Personas</div>
        <nav class="nav" aria-label="Paginas do resultado">
            <a href="#map" data-route="map">Mapa</a>
            <a href="#apoio" data-route="apoio">Apoio</a>
        </nav>
    </header>
    <main>
        <section id="map" class="page plot-panel" data-page="map">
            {plot_markup}
        </section>
        <section id="apoio" class="page support-page" data-page="apoio">
            <div class="support-intro">
                <h1>Apoio</h1>
                <p>Escolha uma rota de apoio financeiro ou escaneie um QR code configurado por voce.</p>
            </div>
            {support_markup}
        </section>
    </main>
    <script>
        const routes = Array.from(document.querySelectorAll("[data-route]"));
        const pages = Array.from(document.querySelectorAll("[data-page]"));

        function showRoute() {{
            const route = window.location.hash.replace("#", "") || "map";
            const activeRoute = route === "apoio" ? "apoio" : "map";

            for (const page of pages) {{
                page.classList.toggle("is-active", page.dataset.page === activeRoute);
            }}

            for (const link of routes) {{
                if (link.dataset.route === activeRoute) {{
                    link.setAttribute("aria-current", "page");
                }} else {{
                    link.removeAttribute("aria-current");
                }}
            }}

            window.dispatchEvent(new Event("resize"));
        }}

        window.addEventListener("hashchange", showRoute);
        showRoute();
    </script>
</body>
</html>
"""
