-- 1. Top 5 funds by AUM
SELECT scheme_name, aum_crore 
FROM dim_fund 
ORDER BY aum_crore DESC LIMIT 5;

-- 2. Average NAV per month
SELECT strftime('%Y-%m', nav_date) as month, 
       ROUND(AVG(nav), 2) as avg_nav
FROM fact_nav 
GROUP BY month ORDER BY month;

-- 3. SIP inflow YoY growth
SELECT strftime('%Y', month) as year,
       ROUND(SUM(inflow_crore), 2) as total_inflow
FROM fact_sip_inflows 
GROUP BY year ORDER BY year;

-- 4. Transactions by type
SELECT transaction_type, 
       COUNT(*) as count,
       ROUND(SUM(amount), 2) as total_amount
FROM fact_transactions 
GROUP BY transaction_type;

-- 5. Funds with expense_ratio < 1%
SELECT scheme_name, expense_ratio 
FROM fact_performance 
WHERE expense_ratio < 1.0
ORDER BY expense_ratio;

-- 6. Top 10 NAV gainers (latest vs 1 year ago)
SELECT amfi_code, 
       ROUND(MAX(nav) - MIN(nav), 2) as nav_growth
FROM fact_nav 
WHERE nav_date >= date('now', '-1 year')
GROUP BY amfi_code 
ORDER BY nav_growth DESC LIMIT 10;

-- 7. Monthly average NAV per fund
SELECT amfi_code,
       strftime('%Y-%m', nav_date) as month,
       ROUND(AVG(nav), 2) as avg_nav
FROM fact_nav 
GROUP BY amfi_code, month;

-- 8. Funds with negative Sharpe ratio
SELECT scheme_name, sharpe_ratio 
FROM fact_performance 
WHERE sharpe_ratio < 0;

-- 9. Total AUM by category
SELECT category, 
       ROUND(SUM(aum_crore), 2) as total_aum
FROM dim_fund 
GROUP BY category 
ORDER BY total_aum DESC;

-- 10. Latest NAV for each fund
SELECT amfi_code, 
       MAX(nav_date) as latest_date, 
       nav
FROM fact_nav 
GROUP BY amfi_code;