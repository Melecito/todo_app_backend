from db_config import get_connection

try:
    conn = get_connection()
    print("Conexión exitosa a MySQL")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")


    for table in cursor:
        print("ok", table)
    
    conn.close()


except Exception as e:
    print("Error al conectar")