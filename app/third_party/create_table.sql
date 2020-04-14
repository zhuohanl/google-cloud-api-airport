CREATE TABLE airports (
    id INTEGER(7), 
    ident VARCHAR(20),
    type VARCHAR(20), 
    name VARCHAR(100), 
    latitude_deg DECIMAL(17,15), 
    longitude_deg DECIMAL(18,15),
    elevation_ft INTEGER(10),
    continent VARCHAR(2),
    iso_country VARCHAR(2),
    iso_region VARCHAR(10),
    municipality VARCHAR(50),
    scheduled_service VARCHAR(3),
    gps_code VARCHAR(20),
    iata_code VARCHAR(3),
    local_code VARCHAR(20),
    home_link VARCHAR(2083),
    wikipedia_link VARCHAR(2083),
    keywords VARCHAR(500)
);