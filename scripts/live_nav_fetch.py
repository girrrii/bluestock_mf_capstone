import requests
import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

# Task 4 — Fetch HDFC Top 100 Direct (125497)
print("Fetching HDFC Top 100 Direct NAV...")
r = requests.get("https://api.mfapi.in/mf/125497")
data = r.json()

print(f"Fund: {data['meta']['scheme_name']}")
print(f"Fund House: {data['meta']['fund_house']}")

nav_df = pd.DataFrame(data["data"])
nav_df.columns = ["date", "nav"]
nav_df["scheme_code"] = 125497
nav_df["scheme_name"] = data["meta"]["scheme_name"]
nav_df["nav"] = pd.to_numeric(nav_df["nav"], errors="coerce")
nav_df["date"] = pd.to_datetime(nav_df["date"], format="%d-%m-%Y")
nav_df = nav_df.sort_values("date").reset_index(drop=True)

nav_df.to_csv(RAW / "hdfc_top100_live.csv", index=False)
print(f"Saved {len(nav_df)} records to data/raw/hdfc_top100_live.csv")