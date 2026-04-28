# Data Directory

## Structure

| Folder | Purpose |
|---|---|
| `raw/` | Original, unmodified datasets (CSV, Parquet, JSON) |
| `processed/` | Cleaned, feature-engineered datasets ready for modeling |
| `external/` | Third-party data (census, economic indicators, geo boundaries) |

## Expected Schema

| Column | Type | Description |
|---|---|---|
| `property_id` | string | Unique identifier |
| `sale_price` | float | Final sale price (target variable) |
| `sale_date` | date | Date of sale closing |
| `list_price` | float | Original listing price |
| `square_feet` | int | Total living area in sq ft |
| `lot_size` | float | Lot size in acres |
| `bedrooms` | int | Number of bedrooms |
| `bathrooms` | float | Number of bathrooms (half baths = 0.5) |
| `year_built` | int | Year constructed |
| `garage_spaces` | int | Number of garage spaces |
| `stories` | int | Number of stories |
| `property_type` | string | Single Family, Condo, Townhouse, Multi-Family |
| `neighborhood` | string | Neighborhood or subdivision name |
| `condition` | string | Excellent, Good, Average, Fair, Poor |
| `heating_type` | string | Forced Air, Radiant, Heat Pump, Baseboard |
| `roof_type` | string | Asphalt, Metal, Tile, Slate |
| `zoning` | string | Residential zoning classification |
| `latitude` | float | Property latitude |
| `longitude` | float | Property longitude |
| `zip_code` | string | 5-digit ZIP code |
| `days_on_market` | int | Days from listing to sale |
| `hoa_fee` | float | Monthly HOA fee (0 if none) |

## Data Sources

- **Primary**: MLS export or public county assessor records
- **External**: U.S. Census Bureau, Federal Reserve (FRED), Walk Score API

> Raw data files are excluded from version control via `.gitignore`.
