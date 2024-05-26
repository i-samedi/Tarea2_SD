import psycopg2

# Configuración de la conexión a PostgreSQL
postgres_host = "localhost"
postgres_port = 5432
postgres_db = "ikea"
postgres_user = "tiago"
postgres_password = "tarea11"

def get_connection():
    conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        database=postgres_db,
        user=postgres_user,
        password=postgres_password
    )
    return conn

# def insert_data(data):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "INSERT INTO Product (product, category, price, correo) VALUES (%s, %s, %s, %s)"
#     cursor.execute(sql, (data["producto"], data["categoria"], data["precio"], data["correo"]))
#     conn.commit()
#     cursor.close()
#     conn.close()