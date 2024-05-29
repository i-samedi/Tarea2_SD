CREATE DATABASE ikea;

\c ikea

CREATE TABLE productos(
    ID SERIAL PRIMARY KEY,
    PRODUCTO VARCHAR(100),
    CATEGORIA VARCHAR(100),
    PRECIO FLOAT,
    CORREO VARCHAR(100)
);

-- Importar datos de productos.csv a la tabla PRODUCTOS
COPY productos(ID,PRODUCTO, CATEGORIA, PRECIO, CORREO)
FROM '/docker-entrypoint-initdb.d/productos.csv'
DELIMITER ';'
CSV HEADER;
