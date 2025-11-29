from __future__ import annotations
from typing import Dict, Any, List


def _format_crypto(crypto_top: List[Dict[str, Any]]) -> str:
    """
    Builds a short bullet list for the top crypto movers.
    """
    if not crypto_top:
        return "No crypto assets breached the alert threshold today."

    lines = ["Top crypto movers (24h):"]
    for item in crypto_top:
        lines.append(
            f"- {item['id'].title()}: {item['pct_change_24h']:.2f}% "
            f"(price: ${item['price_usd']:.2f})"
        )
    return "\n".join(lines)


def _format_fx(fx_top: List[Dict[str, Any]]) -> str:
    """
    Builds a short bullet list for the top FX movers.
    """
    if not fx_top:
        return "No FX pairs breached the alert threshold today."

    lines = ["Top FX movers (1d vs EUR):"]
    for item in fx_top:
        lines.append(
            f"- {item['symbol']}: {item['pct_change_1d']:.2f}% "
            f"(rate: {item['rate_eur']:.4f}, date: {item['date']})"
        )
    return "\n".join(lines)


def build_rule_based_summary(snapshot: Dict[str, Any]) -> str:
    """
    Generates a plain-text summary based purely on rule-based movers.
    This forms the baseline for the AI reasoning layer later.
    """
    crypto_top = snapshot.get("crypto_top", [])
    fx_top = snapshot.get("fx_top", [])

    sections = [
        _format_crypto(crypto_top),
        "",
        _format_fx(fx_top),
    ]

    return "\n".join(sections).strip()
