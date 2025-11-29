from src.market_agent import run_once

if __name__ == "__main__":
    snapshot = run_once()
    print("Agent run completed.")
    print(snapshot)
