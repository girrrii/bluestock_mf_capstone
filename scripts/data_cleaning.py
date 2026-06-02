import pandas as pd
import numpy as np
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

# ── 1. CLEAN NAV HISTORY ─────────────────────────────────────────────
print("Cleaning nav_history...")
nav = pd.read_csv(RAW / "02_nav_history.csv")
print(f"  Raw shape: {nav.shape}")
print(f"  Columns: {list(nav.columns)}")

code_col = "amfi_code" if "amfi_code" in nav.columns else "scheme_code"

nav["date"] = pd.to_datetime(nav["date"], dayfirst=True, errors="coerce")
nav = nav.sort_values([code_col, "date"]).reset_index(drop=True)
nav = nav.drop_duplicates(subset=[code_col, "date"])
nav = nav.set_index("date")
nav = nav.groupby(code_col).apply(
    lambda x: x.reindex(
        pd.date_range(x.index.min(), x.index.max(), freq="D")
    ).ffill()
).reset_index(level=0, drop=True).reset_index()
nav.rename(columns={"index": "date"}, inplace=True)
nav = nav[nav["nav"] > 0]
print(f"  Clean shape: {nav.shape}")
nav.to_csv(PROCESSED / "clean_nav.csv", index=False)
print("  Saved clean_nav.csv")

# ── 2. CLEAN INVESTOR TRANSACTIONS ───────────────────────────────────
print("\nCleaning investor_transactions...")
txn = pd.read_csv(RAW / "08_investor_transactions.csv")
print(f"  Raw shape: {txn.shape}")
txn.columns = txn.columns.str.strip().str.lower().str.replace(" ", "_")
if "transaction_type" in txn.columns:
    txn["transaction_type"] = txn["transaction_type"].str.strip().str.title()
    txn["transaction_type"] = txn["transaction_type"].replace({
        "Sip": "SIP", "Lumpsum": "Lumpsum", "Redemption": "Redemption"
    })
if "amount" in txn.columns:
    txn = txn[pd.to_numeric(txn["amount"], errors="coerce") > 0]
for col in txn.columns:
    if "date" in col:
        txn[col] = pd.to_datetime(txn[col], dayfirst=True, errors="coerce")
txn = txn.drop_duplicates()
print(f"  Clean shape: {txn.shape}")
txn.to_csv(PROCESSED / "clean_transactions.csv", index=False)
print("  Saved clean_transactions.csv")

# ── 3. CLEAN SCHEME PERFORMANCE ──────────────────────────────────────
print("\nCleaning scheme_performance...")
perf = pd.read_csv(RAW / "07_scheme_performance.csv")
print(f"  Raw shape: {perf.shape}")
perf.columns = perf.columns.str.strip().str.lower().str.replace(" ", "_")
for col in perf.columns:
    if "return" in col or "ratio" in col or "sharpe" in col:
        perf[col] = pd.to_numeric(perf[col], errors="coerce")
if "sharpe_ratio" in perf.columns:
    perf["negative_sharpe_flag"] = perf["sharpe_ratio"] < 0
    print(f"  Negative Sharpe flags: {perf['negative_sharpe_flag'].sum()}")
if "expense_ratio" in perf.columns:
    out_of_range = perf[(perf["expense_ratio"] < 0.1) | (perf["expense_ratio"] > 2.5)]
    print(f"  Expense ratio out of range: {len(out_of_range)}")
perf = perf.drop_duplicates()
print(f"  Clean shape: {perf.shape}")
perf.to_csv(PROCESSED / "clean_performance.csv", index=False)
print("  Saved clean_performance.csv")

# ── 4. CLEAN REMAINING DATASETS ──────────────────────────────────────
other_files = {
    "01_fund_master.csv":          "clean_fund_master.csv",
    "03_aum_by_fund_house.csv":    "clean_aum.csv",
    "04_monthly_sip_inflows.csv":  "clean_sip_inflows.csv",
    "05_category_inflows.csv":     "clean_category_inflows.csv",
    "06_industry_folio_count.csv": "clean_folio_count.csv",
    "09_portfolio_holdings.csv":   "clean_portfolio_holdings.csv",
    "10_benchmark_indices.csv":    "clean_benchmark.csv",
}

for raw_file, clean_file in other_files.items():
    try:
        df = pd.read_csv(RAW / raw_file)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df = df.drop_duplicates()
        df = df.dropna(how="all")
        df.to_csv(PROCESSED / clean_file, index=False)
        print(f"  {raw_file} → {clean_file} {df.shape}")
    except FileNotFoundError:
        print(f"  MISSING: {raw_file}")

print("\nAll cleaning done!")