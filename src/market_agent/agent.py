from __future__ import annotations
from typing import Dict, Any, List
from datetime import datetime, timezone

from .data_sources import fetch_crypto_simple
from .fx_data import fetch_fx_rates
from .anomaly import detect_top_movers
from .summary import build_rule_based_summary
from .utils import ensure_dirs, save_json, save_text


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
    Market Data Agent execution:
    - fetches crypto and FX
    - detects top movers
    - builds a rule-based summary
    - persists snapshot and summary to disk
    """
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat(timespec="seconds")
    run_date = now.date().isoformat()  # <-- this line defines run_date

    ensure_dirs("data", "out")

    snapshot: Dict[str, Any] = {
        "as_of": timestamp,
        "status": "ok",
    }

    # --- Crypto ---
    assets = ["bitcoin", "ethereum", "solana"]
    raw_crypto = fetch_crypto_simple(assets)
    crypto = _normalise_crypto(raw_crypto)

    snapshot["crypto"] = crypto

        # Threshold kept simple for now; can be made configurable later.
    crypto_top = detect_top_movers(
        items=crypto,
        pct_key="pct_change_24h",
        threshold=5.0,  # 5% move in 24 hours
        top_n=3,
    )
    snapshot["crypto_top"] = crypto_top
  
    # --- FX ---
    fx_symbols = ["USD", "GBP", "INR"]
    fx_rates = fetch_fx_rates(fx_symbols)
    snapshot["fx"] = fx_rates

    fx_top = detect_top_movers(
        items=fx_rates,
        pct_key="pct_change_1d",
        threshold=0.5,  # 0.5% move against EUR
        top_n=3,
    )
    snapshot["fx_top"] = fx_top

    # --- Rule-based summary ---
    summary_text = build_rule_based_summary(snapshot)
    snapshot["rule_summary"] = summary_text

    # --- Persist outputs ---
    json_path = f"data/snapshot-{run_date}.json"
    summary_path = f"out/summary-{run_date}.md"

    save_json(snapshot, json_path)
    save_text(summary_text, summary_path)

    snapshot["outputs"] = {
        "snapshot_json": json_path,
        "summary_markdown": summary_path,
    }

    snapshot["message"] = "Fetched data, detected movers, built summary and saved outputs."

    return snapshot
