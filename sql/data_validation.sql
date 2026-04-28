-- Null/missing value counts per column
SELECT COUNT(*) AS total_rows,
    SUM(CASE WHEN sale_price IS NULL THEN 1 ELSE 0 END) AS null_price,
    SUM(CASE WHEN square_feet IS NULL THEN 1 ELSE 0 END) AS null_sqft,
    SUM(CASE WHEN bedrooms IS NULL THEN 1 ELSE 0 END) AS null_beds,
    SUM(CASE WHEN bathrooms IS NULL THEN 1 ELSE 0 END) AS null_baths,
    SUM(CASE WHEN year_built IS NULL THEN 1 ELSE 0 END) AS null_year,
    SUM(CASE WHEN neighborhood IS NULL THEN 1 ELSE 0 END) AS null_neighborhood,
    SUM(CASE WHEN zip_code IS NULL THEN 1 ELSE 0 END) AS null_zip
FROM listings;

-- Logical consistency checks
SELECT property_id, sale_price, list_price, square_feet, bedrooms, bathrooms, year_built,
    CASE
        WHEN sale_price <= 0 THEN 'INVALID_PRICE'
        WHEN square_feet <= 0 THEN 'INVALID_SQFT'
        WHEN bedrooms <= 0 THEN 'INVALID_BEDS'
        WHEN year_built < 1700 OR year_built > 2026 THEN 'INVALID_YEAR'
        WHEN sale_price > list_price * 2 THEN 'PRICE_EXCEEDS_2X_LIST'
        WHEN sale_price / square_feet > 2000 THEN 'EXTREME_PRICE_PER_SQFT'
        WHEN days_on_market < 0 THEN 'NEGATIVE_DOM'
    END AS validation_flag
FROM listings
WHERE sale_price <= 0 OR square_feet <= 0 OR bedrooms <= 0
   OR year_built < 1700 OR year_built > 2026
   OR sale_price > list_price * 2
   OR sale_price / square_feet > 2000
   OR days_on_market < 0;

-- Duplicate property detection
SELECT property_id, sale_date, sale_price, COUNT(*) AS occurrence_count
FROM listings GROUP BY property_id, sale_date, sale_price
HAVING COUNT(*) > 1 ORDER BY occurrence_count DESC;

-- Date range validation
SELECT MIN(sale_date) AS earliest_sale, MAX(sale_date) AS latest_sale,
    COUNT(DISTINCT strftime('%Y', sale_date)) AS years_covered,
    COUNT(DISTINCT strftime('%Y-%m', sale_date)) AS months_covered
FROM listings;
