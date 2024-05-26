-- crea la base de datos
CREATE DATABASE Amazon;
-- conecta a la base de datos
\c cars;
-- crea la tabla
CREATE TABLE Product (
    products VARCHAR(100),
    reviews BIGINT,
    price FLOAT
);

COPY Product 
FROM 'db/amazon.csv' 
DELIMITER ';' 
CSV HEADER;

-- CREATE ROLE tiago WITH LOGIN PASSWORD 'tarea11';
-- GRANT ALL PRIVILEGES ON DATABASE tarea1 TO tiago;
