import os
import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv


load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **dbconfig
    )
    print("Pool de conexiones creado correctamente.")

except Error as e:
    print(f"Error al crear el pool de conexiones: {e}")
    connection_pool = None


def get_connection():
    try:
        if connection_pool:
            connection = connection_pool.get_connection()
            return connection
        else:
            raise Error("El pool de conexiones no esta disponible.")

    except Error as e:
        print(f"Error al obtener conexion: {e}")
        return None