import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")

sharpe_df = pd.read_csv(PROCESSED / "sharpe_values.csv")

def recommend_funds(risk_appetite: str):
    """
    Input: risk_appetite — 'Low', 'Moderate', or 'High'
    Output: Top 3 funds by Sharpe ratio within the risk band
    """
    risk_map = {
        "Low":      (0, 0.5),
        "Moderate": (0.5, 1.0),
        "High":     (1.0, 999)
    }
    if risk_appetite not in risk_map:
        print("Invalid input. Choose: Low, Moderate, High")
        return

    low, high = risk_map[risk_appetite]
    filtered = sharpe_df[
        (sharpe_df["sharpe_ratio"] >= low) &
        (sharpe_df["sharpe_ratio"] < high)
    ].sort_values("sharpe_ratio", ascending=False).head(3)

    print(f"\nTop 3 funds for {risk_appetite} risk appetite:")
    print(filtered.to_string(index=False))
    return filtered

if __name__ == "__main__":
    for risk in ["Low", "Moderate", "High"]:
        recommend_funds(risk)