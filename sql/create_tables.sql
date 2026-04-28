CREATE TABLE IF NOT EXISTS listings (
    property_id     TEXT PRIMARY KEY,
    sale_price      REAL NOT NULL,
    list_price      REAL,
    sale_date       DATE NOT NULL,
    square_feet     INTEGER,
    lot_size        REAL,
    bedrooms        INTEGER,
    bathrooms       REAL,
    year_built      INTEGER,
    garage_spaces   INTEGER DEFAULT 0,
    stories         INTEGER DEFAULT 1,
    property_type   TEXT CHECK (property_type IN ('Single Family','Condo','Townhouse','Multi-Family')),
    neighborhood    TEXT,
    condition       TEXT CHECK (condition IN ('Excellent','Good','Average','Fair','Poor')),
    heating_type    TEXT,
    roof_type       TEXT,
    zoning          TEXT,
    latitude        REAL,
    longitude       REAL,
    zip_code        TEXT,
    days_on_market  INTEGER,
    hoa_fee         REAL DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS neighborhoods (
    neighborhood_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    city            TEXT,
    county          TEXT,
    state           TEXT DEFAULT 'OH',
    median_income   REAL,
    population      INTEGER,
    school_rating   REAL,
    walk_score      INTEGER,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id     TEXT REFERENCES listings(property_id),
    model_name      TEXT NOT NULL,
    predicted_price REAL NOT NULL,
    actual_price    REAL,
    prediction_error REAL,
    pct_error       REAL,
    predicted_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_snapshots (
    snapshot_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date   DATE NOT NULL,
    zip_code        TEXT,
    median_price    REAL,
    avg_price       REAL,
    total_sales     INTEGER,
    avg_days_on_market INTEGER,
    inventory_count INTEGER,
    price_per_sqft  REAL,
    yoy_change_pct  REAL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_listings_sale_date ON listings(sale_date);
CREATE INDEX IF NOT EXISTS idx_listings_zip ON listings(zip_code);
CREATE INDEX IF NOT EXISTS idx_listings_neighborhood ON listings(neighborhood);
CREATE INDEX IF NOT EXISTS idx_listings_property_type ON listings(property_type);
CREATE INDEX IF NOT EXISTS idx_listings_price ON listings(sale_price);
CREATE INDEX IF NOT EXISTS idx_snapshots_date_zip ON market_snapshots(snapshot_date, zip_code);
CREATE INDEX IF NOT EXISTS idx_predictions_property ON predictions(property_id);
