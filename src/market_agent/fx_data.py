from __future__ import annotations
from typing import Dict, Any, List
import requests
import xml.etree.ElementTree as ET


ECB_90_DAY_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"


def fetch_fx_rates(symbols: List[str]) -> List[Dict[str, Any]]:
    """
    Fetches the last 90 days of EUR-based FX rates from the ECB.
    Extracts the latest and previous values for the requested currencies.
    """
    resp = requests.get(ECB_90_DAY_URL, timeout=20)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)

    # The XML contains multiple <Cube time="YYYY-MM-DD"> entries.
    daily_rates = []  # each item: (date, { "USD": 1.09, "GBP": ... })

    for cube in root.iter():
        if cube.attrib.get("time"):
            date = cube.attrib["time"]
            rates = {}
            for child in cube:
                rates[child.attrib["currency"]] = float(child.attrib["rate"])
            daily_rates.append((date, rates))

    # Sort by date (newest first)
    daily_rates.sort(reverse=True)

    latest_date, latest_rates = daily_rates[0]
    prev_date, prev_rates = daily_rates[1]

    results = []
    for sym in symbols:
        if sym not in latest_rates:
            continue

        latest = latest_rates[sym]
        prev = prev_rates.get(sym, latest)
        pct_change = ((latest - prev) / prev) * 100 if prev != 0 else 0.0

        results.append(
            {
                "symbol": sym,
                "rate_eur": latest,
                "pct_change_1d": pct_change,
                "date": latest_date,
            }
        )

    return results
