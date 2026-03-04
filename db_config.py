import os
from mysql.connector import pooling, Error
from dotenv import load_dotenv

load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME"),
    "port": 3306
}

connection_pool = None


def get_pool():
    global connection_pool

    if connection_pool is None:
        try:
            connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                **dbconfig
            )
            print("✅ Pool creado correctamente.")
        except Error as e:
            print(f"❌ Error creando pool: {e}")
            raise

    return connection_pool


def get_connection():
    try:
        pool = get_pool()
        return pool.get_connection()
    except Error as e:
        raise Error(f"Error obteniendo conexión: {e}")


def query_example():
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 1")
            return cursor.fetchone()
    except Error as e:
        print(f"Error en consulta: {e}")
        return {"error": "Error en base de datos"}
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    try:
        print(query_example())
    except Exception:
        print("No se pudo conectar a la base de datos.")