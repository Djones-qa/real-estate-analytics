-- Monthly median price trend
SELECT strftime('%Y-%m', sale_date) AS sale_month, COUNT(*) AS total_sales,
    ROUND(AVG(sale_price), 0) AS avg_price,
    ROUND(AVG(sale_price / square_feet), 2) AS avg_price_per_sqft,
    ROUND(AVG(days_on_market), 0) AS avg_dom
FROM listings GROUP BY strftime('%Y-%m', sale_date) ORDER BY sale_month;

-- Year-over-year price change by ZIP code
WITH yearly AS (
    SELECT zip_code, strftime('%Y', sale_date) AS sale_year,
        ROUND(AVG(sale_price), 0) AS avg_price, COUNT(*) AS sale_count
    FROM listings GROUP BY zip_code, strftime('%Y', sale_date)
)
SELECT curr.zip_code, curr.sale_year AS current_year, curr.avg_price AS current_avg,
    prev.avg_price AS prior_avg,
    ROUND((curr.avg_price - prev.avg_price) / prev.avg_price * 100, 2) AS yoy_pct_change
FROM yearly curr JOIN yearly prev
    ON curr.zip_code = prev.zip_code
    AND CAST(curr.sale_year AS INTEGER) = CAST(prev.sale_year AS INTEGER) + 1
ORDER BY curr.zip_code, curr.sale_year;

-- Seasonal price patterns
SELECT CASE CAST(strftime('%m', sale_date) AS INTEGER)
        WHEN 1 THEN 'Q1' WHEN 2 THEN 'Q1' WHEN 3 THEN 'Q1'
        WHEN 4 THEN 'Q2' WHEN 5 THEN 'Q2' WHEN 6 THEN 'Q2'
        WHEN 7 THEN 'Q3' WHEN 8 THEN 'Q3' WHEN 9 THEN 'Q3'
        WHEN 10 THEN 'Q4' WHEN 11 THEN 'Q4' WHEN 12 THEN 'Q4'
    END AS quarter,
    COUNT(*) AS sales_count, ROUND(AVG(sale_price), 0) AS avg_price,
    ROUND(AVG(days_on_market), 0) AS avg_dom
FROM listings WHERE list_price > 0 GROUP BY quarter ORDER BY quarter;

-- Rolling 3-month average DOM
WITH monthly_dom AS (
    SELECT strftime('%Y-%m', sale_date) AS sale_month,
        ROUND(AVG(days_on_market), 0) AS avg_dom, COUNT(*) AS sales
    FROM listings GROUP BY strftime('%Y-%m', sale_date)
)
SELECT sale_month, avg_dom, sales,
    ROUND(AVG(avg_dom) OVER (ORDER BY sale_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS rolling_3m_dom
FROM monthly_dom ORDER BY sale_month;

-- Price band distribution over time
SELECT strftime('%Y', sale_date) AS sale_year,
    CASE WHEN sale_price < 100000 THEN 'Under 100K'
         WHEN sale_price < 200000 THEN '100K-200K'
         WHEN sale_price < 300000 THEN '200K-300K'
         WHEN sale_price < 500000 THEN '300K-500K'
         ELSE '500K+' END AS price_band,
    COUNT(*) AS count
FROM listings GROUP BY sale_year, price_band ORDER BY sale_year;
