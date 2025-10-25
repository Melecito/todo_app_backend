import os
import mysql.connector
from mysql.connector import pooling, Error
# Importar dotenv es correcto, pero recuerda que en la nube (Render/Railway) no se usa.
# from dotenv import load_dotenv # Se recomienda comentar o eliminar esta línea en producción.

# 1. CARGA DE VARIABLES DE ENTORNO (Comentado para Railway/Render)

# 2. CONFIGURACIÓN DEL POOL
# Se obtienen las credenciales de las variables de entorno inyectadas por Railway (prefijo MYSQL_)
dbconfig = {
    # 🚨 CRÍTICO: Usar variables inyectadas por Railway
    "host": os.getenv("MYSQL_HOST"), 
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"), # Railway usa MYSQL_PASSWORD
    "database": os.getenv("MYSQL_DATABASE"), # Railway usa MYSQL_DATABASE
    "port": os.getenv("MYSQL_PORT") # Usar el puerto inyectado para la conexión interna
}

# Inicializamos el pool como None
connection_pool = None

try:
    # 3. CREACIÓN DEL POOL DE CONEXIONES
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,  # Tamaño del pool, ajusta según sea necesario
        **dbconfig
    )
    print("Pool de conexiones creado correctamente. ¡Servidor listo!")

except Error as e:
    # Si la conexión inicial falla (credenciales, firewall o variables nulas)
    print(f"Error CRÍTICO al crear el pool de conexiones. Revise sus variables de entorno o la conexión de DB: {e}")
    pass 

# 4. FUNCIÓN PARA OBTENER CONEXIÓN
def get_connection():
    """
    Intenta obtener una conexión del pool. 
    Lanza una excepción si el pool no está disponible.
    """
    if connection_pool is None:
        raise Error("El pool de conexiones no esta disponible. (Revisar credenciales o logs de Railway)")

    try:
        connection = connection_pool.get_connection()
        return connection
    except Error as e:
        raise Error(f"Error al obtener conexión del pool: {e}")


# 5. FUNCIÓN DE USO EN LA APLICACIÓN (Ejemplo conceptual)
def query_example():
    connection = None  
    try:
        connection = get_connection()
        
        # El 'with' ahora solo se ejecuta si 'connection' es un objeto válido
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 1")
            result = cursor.fetchone()
            return result
            
    except Error as e:
        print(f"Error en la consulta: {e}")
        return {"error": "Conexión de base de datos fallida o consulta errónea"}
        
    finally:
        # CRÍTICO: Devolver la conexión al pool
        if connection and connection.is_connected():
            connection.close()

# Si quieres probar la conexión al inicio (opcional)
if __name__ == '__main__':
    if connection_pool:
        print(f"Resultado de consulta de prueba: {query_example()}")
    else:
        print("El pool no pudo ser inicializado. La aplicación fallará.")