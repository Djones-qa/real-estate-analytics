-- Price statistics by neighborhood
SELECT neighborhood, COUNT(*) AS total_sales,
    ROUND(AVG(sale_price), 0) AS avg_price,
    ROUND(MIN(sale_price), 0) AS min_price, ROUND(MAX(sale_price), 0) AS max_price,
    ROUND(AVG(sale_price / square_feet), 2) AS avg_price_per_sqft,
    ROUND(AVG(days_on_market), 0) AS avg_dom
FROM listings GROUP BY neighborhood HAVING COUNT(*) >= 5 ORDER BY avg_price DESC;

-- Price by property type and condition
SELECT property_type, condition, COUNT(*) AS sales,
    ROUND(AVG(sale_price), 0) AS avg_price,
    ROUND(AVG(sale_price / square_feet), 2) AS avg_ppsf,
    ROUND(AVG(days_on_market), 0) AS avg_dom
FROM listings GROUP BY property_type, condition ORDER BY property_type, avg_price DESC;

-- Bedroom/bathroom premium analysis
SELECT bedrooms, ROUND(AVG(bathrooms), 1) AS avg_baths, COUNT(*) AS count,
    ROUND(AVG(sale_price), 0) AS avg_price,
    ROUND(AVG(sale_price / square_feet), 2) AS avg_ppsf
FROM listings WHERE bedrooms BETWEEN 1 AND 6 GROUP BY bedrooms ORDER BY bedrooms;

-- HOA impact on pricing
SELECT CASE
        WHEN hoa_fee = 0 OR hoa_fee IS NULL THEN 'No HOA'
        WHEN hoa_fee < 200 THEN 'Low (1-199)'
        WHEN hoa_fee < 400 THEN 'Medium (200-399)'
        ELSE 'High (400+)' END AS hoa_tier,
    COUNT(*) AS count, ROUND(AVG(sale_price), 0) AS avg_price,
    ROUND(AVG(days_on_market), 0) AS avg_dom
FROM listings GROUP BY hoa_tier ORDER BY avg_price;

-- Property age impact on value
SELECT CASE
        WHEN (CAST(strftime('%Y', sale_date) AS INT) - year_built) <= 5 THEN '0-5 years'
        WHEN (CAST(strftime('%Y', sale_date) AS INT) - year_built) <= 15 THEN '6-15 years'
        WHEN (CAST(strftime('%Y', sale_date) AS INT) - year_built) <= 30 THEN '16-30 years'
        WHEN (CAST(strftime('%Y', sale_date) AS INT) - year_built) <= 50 THEN '31-50 years'
        ELSE '50+ years' END AS age_group,
    COUNT(*) AS count, ROUND(AVG(sale_price), 0) AS avg_price,
    ROUND(AVG(sale_price / square_feet), 2) AS avg_ppsf
FROM listings WHERE year_built IS NOT NULL GROUP BY age_group;
