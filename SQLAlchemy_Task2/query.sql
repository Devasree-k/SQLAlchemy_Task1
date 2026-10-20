
CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE,
    license_number VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE transport_collection (
    id SERIAL PRIMARY KEY,
    driver_id INTEGER NOT NULL
        REFERENCES drivers(id),
    vehicle_number VARCHAR(20) NOT NULL,
    collection_date DATE NOT NULL,
    morning_trips INTEGER NOT NULL CHECK (morning_trips >= 0),
    evening_trips INTEGER NOT NULL CHECK (evening_trips >= 0),
    morning_collection NUMERIC(10, 2) NOT NULL
        CHECK (morning_collection >= 0),
    evening_collection NUMERIC(10, 2) NOT NULL
        CHECK (evening_collection >= 0),
    fuel_expense NUMERIC(10, 2) NOT NULL
        CHECK (fuel_expense >= 0),
    other_expense NUMERIC(10, 2) NOT NULL
        CHECK (other_expense >= 0),
    total_trips INTEGER NOT NULL,
    total_collection NUMERIC(10, 2) NOT NULL,
    total_expense NUMERIC(10, 2) NOT NULL,
    net_collection NUMERIC(10, 2) NOT NULL,
    report_file TEXT
);

CREATE INDEX ix_collection_driver_id
    ON transport_collection(driver_id);

-- Example: get collection records with driver details.
SELECT
    tc.id,
    tc.collection_date,
    tc.vehicle_number,
    tc.total_collection,
    tc.net_collection,
    d.id AS driver_id,
    d.name AS driver_name,
    d.license_number
FROM transport_collection AS tc
JOIN drivers AS d
    ON tc.driver_id = d.id
ORDER BY tc.collection_date DESC;
