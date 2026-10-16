CREATE TABLE transport_collection (
    id SERIAL PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    vehicle_number VARCHAR(20) NOT NULL,
    collection_date DATE NOT NULL,
    morning_trips INTEGER NOT NULL,
    evening_trips INTEGER NOT NULL,
    morning_collection NUMERIC(10, 2) NOT NULL,
    evening_collection NUMERIC(10, 2) NOT NULL,
    fuel_expense NUMERIC(10, 2) NOT NULL,
    other_expense NUMERIC(10, 2) NOT NULL,
    total_trips INTEGER NOT NULL,
    total_collection NUMERIC(10, 2) NOT NULL,
    total_expense NUMERIC(10, 2) NOT NULL,
    net_collection NUMERIC(10, 2) NOT NULL,
    report_file TEXT
);

SELECT * FROM transport_collection


CREATE PROCEDURE create_transport_collection(
    IN p_driver_name VARCHAR(100),
    IN p_vehicle_number VARCHAR(20),
    IN p_collection_date DATE,
    IN p_morning_trips INTEGER,
    IN p_evening_trips INTEGER,
    IN p_morning_collection NUMERIC(10, 2),
    IN p_evening_collection NUMERIC(10, 2),
    IN p_fuel_expense NUMERIC(10, 2),
    IN p_other_expense NUMERIC(10, 2),
    INOUT p_collection_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO transport_collection (
    driver_name,
    vehicle_number,
    collection_date,
    morning_trips,
    evening_trips,
    morning_collection,
    evening_collection,
    fuel_expense,
    other_expense,
    total_trips,
    total_collection,
    total_expense,
    net_collection
    )
    VALUES (
    p_driver_name,
    p_vehicle_number,
    p_collection_date,
    p_morning_trips,
    p_evening_trips,
    p_morning_collection,
    p_evening_collection,
    p_fuel_expense,
    p_other_expense,
    p_morning_trips + p_evening_trips,
    p_morning_collection + p_evening_collection,
    p_fuel_expense + p_other_expense,
    (p_morning_collection + p_evening_collection)
        - (p_fuel_expense + p_other_expense)
    )
    RETURNING id INTO p_collection_id;
END;
$$;