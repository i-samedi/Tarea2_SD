-- crea la base de datos
CREATE DATABASE IKEA;
-- conecta a la base de datos
\c IKEA;
-- crea la tabla
CREATE TABLE Product (
    id SERIAL PRIMARY KEY,
    product VARCHAR(100),
    category VARCHAR(100),
    price FLOAT,
    correo VARCHAR(100)
);

COPY Product 
FROM 'db/Productos_IKEA.csv' 
DELIMITER ';' 
CSV HEADER;

--\copy Product FROM 'C:\Users\FelipitoChiLL\Documents\GitHub\Tarea2_SD\db\amazon.csv' WITH (DELIMITER ';', FORMAT csv, HEADER true);
--\copy Product FROM '/Users/lordsamedi/Documents/GitHub/Tarea2_SD/db/Productos_IKEA.csv' WITH (DELIMITER ';', FORMAT csv, HEADER true);

-- CREATE ROLE tiago WITH LOGIN PASSWORD 'tarea11';
-- GRANT ALL PRIVILEGES ON DATABASE ikea TO tiago;
