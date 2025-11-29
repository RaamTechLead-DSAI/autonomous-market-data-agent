from __future__ import annotations
from typing import List, Dict, Any


def detect_top_movers(
    items: List[Dict[str, Any]],
    pct_key: str,
    threshold: float,
    top_n: int = 3,
) -> List[Dict[str, Any]]:
    """
    Filters and sorts items by absolute percentage change.
    Keeps only entries that cross the given threshold.
    """
    flagged = [
        item for item in items
        if abs(float(item.get(pct_key, 0.0))) >= threshold
    ]

    # Sort in descending order of absolute movement.
    flagged.sort(key=lambda x: abs(float(x.get(pct_key, 0.0))), reverse=True)

    return flagged[:top_n]
