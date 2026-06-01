import requests
import pandas as pd
import os

# 5 schemes to fetch
schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

os.makedirs("data/raw", exist_ok=True)

for name, code in schemes.items():
    print(f"Fetching {name} ({code})...")
    
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    data = response.json()
    
    # Fund info
    scheme_name = data["meta"]["scheme_name"]
    fund_house = data["meta"]["fund_house"]
    print(f"  {scheme_name} — {fund_house}")
    
    # NAV history
    nav_df = pd.DataFrame(data["data"])
    nav_df["scheme_code"] = code
    nav_df["scheme_name"] = scheme_name
    nav_df.columns = ["date", "nav", "scheme_code", "scheme_name"]
    
    # Save to CSV
    filepath = f"data/raw/{name}_nav.csv"
    nav_df.to_csv(filepath, index=False)
    print(f"  Saved {len(nav_df)} records to {filepath}")

print("\nAll NAV data fetched and saved!")