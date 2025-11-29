from __future__ import annotations
from typing import Dict, Any, List
from datetime import datetime, timezone

from .data_sources import fetch_crypto_simple


def _normalise_crypto(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalises CoinGecko's response into a clean list of crypto records.
    Keeps the structure simple for downstream steps in the agent.
    """
    items: List[Dict[str, Any]] = []
    for asset_id, values in raw.items():
        items.append(
            {
                "id": asset_id,
                "price_usd": float(values.get("usd", 0.0)),
                "pct_change_24h": float(values.get("usd_24h_change", 0.0)),
            }
        )
    return items


def run_once() -> Dict[str, Any]:
    """
    First working step of the Market Data Agent.
    Fetches a small set of crypto prices and returns them as a snapshot.
    """
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    snapshot: Dict[str, Any] = {
        "as_of": timestamp,
        "status": "ok",
    }

    # Fetch a small asset list for now; this can be expanded later.
    assets = ["bitcoin", "ethereum", "solana"]
    raw_crypto = fetch_crypto_simple(assets)
    crypto = _normalise_crypto(raw_crypto)

    snapshot["crypto"] = crypto
    snapshot["message"] = "Fetched crypto data from CoinGecko."

    return snapshot
