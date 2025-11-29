from __future__ import annotations
from typing import Dict, Any, List

import requests

COINGECKO_SIMPLE_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_crypto_simple(assets: List[str], vs: str = "usd") -> Dict[str, Any]:
    """
    Fetch simple crypto prices and 24h percentage change from CoinGecko.

    Example response shape:
    {
      "bitcoin": {"usd": 62000.0, "usd_24h_change": 2.5},
      "ethereum": {"usd": 3500.0, "usd_24h_change": -1.2}
    }
    """
    params = {
        "ids": ",".join(assets),
        "vs_currencies": vs,
        "include_24hr_change": "true",
    }
    resp = requests.get(COINGECKO_SIMPLE_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()
