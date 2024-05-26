CREATE TABLE CLIENTES(
    ID SERIAL PRIMARY KEY,
    NOMBRE VARCHAR(255),
    APELLIDO VARCHAR(255),
    CORREO VARCHAR(255)
);

CREATE TABLE PRODUCTOS(
    ID SERIAL PRIMARY KEY,
    CLIENTEID INT REFERENCES CLIENTES(CLIENTEID),
    PRODUCTO VARCHAR(100),
    CATEGORIA VARCHAR(100),
    PRECIO FLOAT,
    CORREO VARCHAR(100)
);

-- docker cp clientes.csv <db_container_id>:/clientes.csv
-- docker cp pedidos.csv <db_container_id>:/pedidos.csv

-- docker exec -it <db_container_id> psql -U postgres -d pedidos

-- -- Importar datos de clientes.csv a la tabla CLIENTES
-- COPY CLIENTES(NOMBRE, APELLIDO, TELEFONO, CORREO)
-- FROM 'db/cliente.csv'
-- DELIMITER ','
-- CSV HEADER;

-- -- Importar datos de pedidos.csv a la tabla PEDIDOS
-- COPY PEDIDOS(CLIENTEID, PRODUCTO, CATEGORIA, PRECIO, ESTADO)
-- FROM 'db/productos.csv'
-- DELIMITER ','
-- CSV HEADER;

-- #-----------------PASO A PASO------------------#  
-- docker ps  # Para listar todos los contenedores en funcionamiento y obtener el ID o nombre del contenedor PostgreSQL
-- docker exec -it <db_container_id> psql -U postgres

-- CREATE DATABASE pedidos;
-- \c pedidos  # Conectar a la base de datos 'pedidos'
-- docker cp init.sql <db_container_id>:/init.sql
-- docker exec -it <db_container_id> psql -U postgres -d pedidos -f /init.sql


-- docker-compose up -d
-- docker exec -it <db_container_id> psql -U postgres -c "CREATE DATABASE pedidos;"
-- docker cp init.sql <db_container_id>:/init.sql
-- docker exec -it <db_container_id> psql -U postgres -d pedidos -f /init.sql

-- python consumer.py









--\copy Product FROM 'C:\Users\FelipitoChiLL\Documents\GitHub\Tarea2_SD\db\amazon.csv' WITH (DELIMITER ';', FORMAT csv, HEADER true);
--\copy Product FROM '/Users/lordsamedi/Documents/GitHub/Tarea2_SD/db/Productos_IKEA.csv' WITH (DELIMITER ';', FORMAT csv, HEADER true);


