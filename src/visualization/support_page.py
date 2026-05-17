from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any


DEFAULT_SUPPORT_CONFIG = Path("config/support/donation_routes.json")


def load_support_routes(config_path: str | Path = DEFAULT_SUPPORT_CONFIG) -> list[dict[str, str]]:
    path = Path(config_path)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    routes = payload.get("routes", payload if isinstance(payload, list) else [])
    if not isinstance(routes, list):
        return []

    normalized: list[dict[str, str]] = []
    for route in routes:
        if not isinstance(route, dict) or route.get("enabled") is False:
            continue

        platform = _string_value(route, "platform", "name")
        url = _string_value(route, "url", "link", "href")
        qr_image = _string_value(route, "qr_image", "qrCode", "qrcode")
        description = _string_value(route, "description", "label")

        if not platform and not url and not qr_image:
            continue

        normalized.append(
            {
                "platform": platform or "Apoio",
                "url": url,
                "qr_image": qr_image,
                "description": description,
            }
        )

    return normalized


def render_support_cards(routes: list[dict[str, str]]) -> str:
    if not routes:
        return """
            <section class="support-empty" aria-live="polite">
                <h2>Nenhuma rota de apoio configurada</h2>
                <p>Adicione suas plataformas de apoio em <code>config/support/donation_routes.json</code> e coloque imagens de QR code em <code>assets/qrcode/</code>.</p>
            </section>
        """

    cards = []
    for route in routes:
        platform = escape(route["platform"])
        description = escape(route.get("description", ""))
        url = escape(route.get("url", ""), quote=True)
        qr_image = escape(route.get("qr_image", ""), quote=True)
        link = (
            f'<a class="support-link" href="{url}" target="_blank" rel="noopener noreferrer">Abrir plataforma</a>'
            if url
            else '<span class="support-muted">Link nao configurado</span>'
        )
        qr = (
            f'<img class="support-qr" src="{qr_image}" alt="QR code para {platform}" loading="lazy" />'
            if qr_image
            else '<div class="support-qr support-qr-placeholder">QR</div>'
        )
        body = f"<p>{description}</p>" if description else ""
        cards.append(
            f"""
            <article class="support-card">
                {qr}
                <div>
                    <h2>{platform}</h2>
                    {body}
                    {link}
                </div>
            </article>
            """
        )

    return "\n".join(cards)


def _string_value(route: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = route.get(key)
        if value is not None:
            return str(value).strip()
    return ""
