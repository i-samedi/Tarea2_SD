import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname='pedidos',
        user='postgres',
        password='password',
        host='localhost',
        port='5432'
    )
    return conn
