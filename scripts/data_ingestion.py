import requests
import pandas as pd
import os
from pathlib import Path

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

print("Fetching fund master from AMFI...")
url = "https://api.mfapi.in/mf"
response = requests.get(url)
fund_master = pd.DataFrame(response.json())
fund_master.columns = ["scheme_code", "scheme_name", "isin_growth", "isin_div_reinvestment"]
fund_master.to_csv(RAW / "fund_master.csv", index=False)
print(f"Fund master: {fund_master.shape} saved")

schemes = {
    "HDFC_Top100":     125497,
    "SBI_Bluechip":    119551,
    "ICICI_Bluechip":  120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip":   119092,
    "Kotak_Bluechip":  120841,
    "Mirae_Largecap":  118825,
    "UTI_Nifty50":     120716,
    "Parag_Flexicap":  122639,
    "DSP_Midcap":      119061
}

all_nav = []

for name, code in schemes.items():
    print(f"Fetching {name} ({code})...")
    r = requests.get(f"https://api.mfapi.in/mf/{code}")
    data = r.json()
    
    df = pd.DataFrame(data["data"])
    df["scheme_code"] = code
    df["scheme_name"] = data["meta"]["scheme_name"]
    df["fund_house"] = data["meta"]["fund_house"]
    df["scheme_category"] = data["meta"]["scheme_category"]
    df.columns = ["date", "nav", "scheme_code", "scheme_name", "fund_house", "scheme_category"]
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df = df.sort_values("date").reset_index(drop=True)
    df.to_csv(RAW / f"{name}_nav.csv", index=False)
    all_nav.append(df)
    print(f"  {len(df)} records saved")

nav_history = pd.concat(all_nav, ignore_index=True)
nav_history.to_csv(RAW / "nav_history.csv", index=False)
print(f"\nCombined nav_history: {nav_history.shape} saved")

print("\n=== DATA QUALITY SUMMARY ===")
print(f"Fund master total schemes: {len(fund_master)}")
print(f"Nav history schemes: {nav_history['scheme_code'].nunique()}")
master_codes = set(fund_master["scheme_code"].astype(str))
nav_codes = set(nav_history["scheme_code"].astype(str))
missing = nav_codes - master_codes
print(f"NAV codes missing from fund_master: {missing if missing else 'None'}")
print(f"Null NAVs: {nav_history['nav'].isnull().sum()}")
print(f"Date range: {nav_history['date'].min()} to {nav_history['date'].max()}")
print("\nDone!")