# Data Dictionary — Bluestock MF Capstone

## dim_fund
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT | Unique AMFI scheme code (PK) |
| scheme_name | TEXT | Full name of the mutual fund scheme |
| fund_house | TEXT | AMC / fund house name |
| category | TEXT | SEBI category (Equity, Debt, Hybrid) |
| sub_category | TEXT | Sub-category (Large Cap, Mid Cap, etc.) |
| expense_ratio | REAL | Annual expense ratio in % |
| risk_grade | TEXT | Risk rating (Low/Moderate/High) |

## fact_nav
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT | FK to dim_fund |
| nav_date | DATE | Date of NAV |
| nav | REAL | Net Asset Value in ₹ |
| daily_return | REAL | Daily % return |

## fact_transactions
| Column | Type | Description |
|---|---|---|
| folio_number | TEXT | Investor folio ID |
| amfi_code | TEXT | FK to dim_fund |
| transaction_date | DATE | Date of transaction |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount | REAL | Transaction amount in ₹ |
| units | REAL | Units purchased/redeemed |
| nav_at_transaction | REAL | NAV on transaction date |

## fact_performance
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT | FK to dim_fund |
| as_of_date | DATE | Performance as of date |
| return_1y | REAL | 1-year return % |
| return_3y | REAL | 3-year CAGR % |
| return_5y | REAL | 5-year CAGR % |
| sharpe_ratio | REAL | Risk-adjusted return |
| beta | REAL | Market sensitivity |
| expense_ratio | REAL | Annual cost in % |

## fact_sip_inflows
| Column | Type | Description |
|---|---|---|
| month | DATE | Month of inflow |
| category | TEXT | Fund category |
| inflow_crore | REAL | SIP inflow in ₹ crore |

## Sources
- NAV data: mfapi.in
- Fund master: AMFI India
- Transactions/Performance: Bluestock_MF_Datasets (provided)