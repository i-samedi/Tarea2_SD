CREATE TABLE PRODUCTOS(
    ID SERIAL PRIMARY KEY,
    PRODUCTO VARCHAR(100),
    CATEGORIA VARCHAR(100),
    PRECIO FLOAT,
    CORREO VARCHAR(100)
);

-- Importar datos de pedidos.csv a la tabla PEDIDOS
COPY PRODUCTOS(ID, PRODUCTO, CATEGORIA, PRECIO, CORREO)
FROM 'db/productos.csv'
DELIMITER ','
CSV HEADER;
