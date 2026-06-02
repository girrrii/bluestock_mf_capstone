import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

PROCESSED = Path("data/processed")
DB = Path("data/db")
DB.mkdir(exist_ok=True)

engine = create_engine("sqlite:///data/db/bluestock_mf.db")

# Load schema
with engine.connect() as conn:
    with open("sql/schema.sql") as f:
        for stmt in f.read().split(";"):
            if stmt.strip():
                conn.execute(text(stmt))
    conn.commit()
print("Schema created")

# Load each cleaned CSV
tables = {
    "clean_fund_master.csv":      "dim_fund",
    "clean_nav.csv":              "fact_nav",
    "clean_transactions.csv":     "fact_transactions",
    "clean_performance.csv":      "fact_performance",
    "clean_sip_inflows.csv":      "fact_sip_inflows",
}

for file, table in tables.items():
    try:
        df = pd.read_csv(PROCESSED / file)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"  Loaded {file} → {table} ({len(df)} rows)")
    except FileNotFoundError:
        print(f"  MISSING: {file}")

print("DB loaded!")