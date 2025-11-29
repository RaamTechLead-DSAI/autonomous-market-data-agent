import json
from src.market_agent import run_once

if __name__ == "__main__":
    snapshot = run_once()

    print("Agent run completed.\n")

    print("----- Rule Summary -----")
    print(snapshot["rule_summary"])
    print()

    print("----- Full Snapshot -----")
    print(json.dumps(snapshot, indent=2))
