import bcrypt
import re
from db_config import get_connection


# --- 🔹 Funciones de validación ---
def validar_email(email: str) -> bool:
    
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None


def validar_longitud(texto: str, minimo: int, maximo: int) -> bool:
    """Valida que el texto esté dentro del rango de longitud permitido."""
    return minimo <= len(texto) <= maximo



class UserModel:
    """Manejo de usuarios: CRUD en base de datos."""

    @staticmethod
    def create_user(data: dict) -> dict:
        """Crea un nuevo usuario en la base de datos."""
        conn = None
        try:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Validaciones
            if not all([username, email, password]):
                return {"error": "Todos los campos son obligatorios."}

            if not validar_email(email):
                return {"error": "Formato de email inválido."}

            if not validar_longitud(password, 6, 30):
                return {"error": "La contraseña debe tener entre 6 y 30 caracteres."}

            # Hashear la contraseña
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            query = """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
            """
            params = (username, email, hashed_password)

            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    return {"success": True, "id": cursor.lastrowid}

        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}

    @staticmethod
    def list_users() -> list:
        """Devuelve la lista de todos los usuarios (sin contraseñas)."""
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT id, username, email FROM users")
                    return cursor.fetchall()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_user(user_id: int) -> dict:
        """Obtiene un usuario por su ID."""
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT id, username, email FROM users WHERE id = %s",
                        (user_id,)
                    )
                    user = cursor.fetchone()
                    return user if user else {"error": "Usuario no encontrado."}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_user(user_id: int, data: dict) -> dict:
        """Actualiza los datos de un usuario."""
        conn = None
        try:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not validar_email(email):
                return {"error": "Formato de email inválido."}

            if password:
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            else:
                hashed_password = None

            query = "UPDATE users SET username = %s, email = %s"
            params = [username, email]

            if hashed_password:
                query += ", password = %s"
                params.append(hashed_password)

            query += " WHERE id = %s"
            params.append(user_id)

            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(params))
                    conn.commit()

                    if cursor.rowcount > 0:
                        return {"success": True, "message": "Usuario actualizado correctamente."}
                    else:
                        return {"error": "Usuario no encontrado."}

        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}

    @staticmethod
    def delete_user(user_id: int) -> dict:
        """Elimina un usuario por su ID."""
        conn = None
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    conn.commit()

                    if cursor.rowcount > 0:
                        return {"success": True, "message": "Usuario eliminado correctamente."}
                    else:
                        return {"error": "Usuario no encontrado."}

        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        
    
    @staticmethod
    def authenticate(email, password):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                    user = cursor.fetchone()

                    if not user:
                        return {"error": "Usuario no encontrado."}
                    
                    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                        return {"error": "Contraseña incorrecta"}
                    
                    return {"success": True, "user": user}
        except Exception as e:
            return {"error": str(e)}

