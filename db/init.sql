-- crea la base de datos
CREATE DATABASE IKEA;
-- conecta a la base de datos
\c IKEA;
-- crea la tabla
CREATE TABLE Product (
    id SERIAL PRIMARY KEY,
    product VARCHAR(100),
    category BIGINT,
    price FLOAT,
    correo VARCHAR(100)
);

COPY Product 
FROM 'db/Productos_IKEA.csv' 
DELIMITER ';' 
CSV HEADER;

-- CREATE ROLE tiago WITH LOGIN PASSWORD 'tarea11';
-- GRANT ALL PRIVILEGES ON DATABASE tarea1 TO tiago;
