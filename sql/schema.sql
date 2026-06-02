CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code TEXT PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    expense_ratio REAL,
    risk_grade TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    nav_date DATE,
    nav REAL,
    daily_return REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    folio_number TEXT,
    amfi_code TEXT,
    transaction_date DATE,
    transaction_type TEXT,
    amount REAL,
    units REAL,
    nav_at_transaction REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    as_of_date DATE,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    sharpe_ratio REAL,
    beta REAL,
    expense_ratio REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_sip_inflows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month DATE,
    category TEXT,
    inflow_crore REAL
);