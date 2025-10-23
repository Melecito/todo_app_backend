import os
import mysql.connector
from mysql.connector import pooling, Error
# Importar dotenv es correcto, pero recuerda que en Render solo usa las variables de entorno.
from dotenv import load_dotenv

# 1. CARGA DE VARIABLES DE ENTORNO (Solo para desarrollo local)
# Render ignora este paso y usa sus propias variables inyectadas.
load_dotenv()

# 2. CONFIGURACIÓN DEL POOL
# Se obtienen las credenciales de las variables de entorno de Render/dotenv
dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

# Inicializamos el pool como None
connection_pool = None

try:
    # 3. CREACIÓN DEL POOL DE CONEXIONES
    # Esto se ejecuta una vez al iniciar el servidor.
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,  # Tamaño del pool, ajusta según sea necesario
        **dbconfig
    )
    print("Pool de conexiones creado correctamente. ¡Servidor listo!")

except Error as e:
    # Si la conexión inicial falla (credenciales o firewall), se imprime el error CRÍTICO.
    # connection_pool se queda como None, que es lo que queremos.
    print(f"Error CRÍTICO al crear el pool de conexiones. Revise sus variables de entorno: {e}")
    # Nota: No asignamos None, ya está inicializado arriba, pero se mantiene la lógica.
    pass # Permite que el servidor continúe imprimiendo el error antes de fallar.

# 4. FUNCIÓN PARA OBTENER CONEXIÓN
def get_connection():
    """
    Intenta obtener una conexión del pool. 
    Lanza una excepción si el pool no está disponible, evitando devolver None.
    """
    if connection_pool is None:
        # Si el pool no existe (porque falló al inicio), lanzamos un error claro.
        raise Error("El pool de conexiones no esta disponible. (Revisar credenciales o logs de Render)")

    try:
        # Intentamos obtener la conexión del pool
        connection = connection_pool.get_connection()
        return connection
    except Error as e:
        # Si hay un error al obtener la conexión (ej. pool vacío), relanzamos el error.
        raise Error(f"Error al obtener conexión del pool: {e}")


# 5. FUNCIÓN DE USO EN LA APLICACIÓN (Ejemplo conceptual)
def query_example():
    connection = None  # Inicializar la variable
    try:
        connection = get_connection()
        
        # El 'with' ahora solo se ejecuta si 'connection' es un objeto válido (no None)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 1")
            result = cursor.fetchone()
            return result
            
    except Error as e:
        # Aquí se capturan los errores de MySQL y los errores lanzados por get_connection().
        print(f"Error en la consulta: {e}")
        # En una aplicación real, se registra el error y se devuelve una respuesta HTTP 500.
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