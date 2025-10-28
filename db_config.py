import os
import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv

load_dotenv()
dbconfig = {
    'host': os.getenv('DB_HOST'), # En AWS será el RDS Endpoint
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'db': os.getenv('DB_NAME'),
    # ...
}


# Inicializamos el pool como None
connection_pool = None

try:
    # CREACIÓN DEL POOL DE CONEXIONES
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=10,
        **dbconfig
        
    )
    print("✅ Pool de conexiones creado correctamente. ¡Servidor listo!")

except Error as e:
    print(f"❌ Error CRÍTICO al crear el pool de conexiones: {e}")
    connection_pool = None


# 4. FUNCIÓN PARA OBTENER CONEXIÓN
def get_connection():
    """
    Intenta obtener una conexión del pool. 
    """
    if connection_pool is None:
        raise Error("El pool de conexiones no esta disponible. (Revisar credenciales o logs de Railway)")

    try:
        connection = connection_pool.get_connection()
        return connection
    except Error as e:
        raise Error(f"Error al obtener conexión del pool: {e}")


# 5. FUNCIÓN DE USO EN LA APLICACIÓN (Se mantiene el código original)
def query_example():
    connection = None 
    try:
        connection = get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 1")
            result = cursor.fetchone()
            return result
            
    except Error as e:
        print(f"Error en la consulta: {e}")
        return {"error": "Conexión de base de datos fallida o consulta errónea"}
        
    finally:
        # Devolver la conexión al pool
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    if connection_pool:
        print(f"Resultado de consulta de prueba: {query_example()}")
    else:
        print("El pool no pudo ser inicializado. La aplicación fallará.")