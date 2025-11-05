from db_config import get_connection

class TaskModel:

    @staticmethod
    def list_tasks(user_id):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT id, title, description, completed, created_at FROM tasks WHERE user_id = %s",
                        (user_id,)
                    )
                    return cursor.fetchall()
        except Exception as e:
            return {"error": str(e)}
        

    @staticmethod
    def create_task(user_id, data):
        try:
            title = data.get("title")
            description =data.get("description", "")

            if not title:
                return {"error": "El titulo es obligatorio"}
            
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO tasks (user_id, title, description) VALUES (%s, %s, %s)",
                        (user_id, title, description)
                    )
                    conn.commit()
                    return {"success": True, "id": cursor.lastrowid}
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def update_task(user_id, task_id, data):
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    fields = []
                    values = []

                    # ✅ Solo agrega los campos que llegan en el body
                    if "title" in data and data["title"] is not None:
                        fields.append("title = %s")
                        values.append(data["title"])

                    if "description" in data and data["description"] is not None:
                        fields.append("description = %s")
                        values.append(data["description"])

                    if "completed" in data:
                        fields.append("completed = %s")
                        values.append(data["completed"])

                    if not fields:
                        return {"error": "No se enviaron campos para actualizar."}

                    # Agrega condiciones WHERE
                    values.extend([task_id, user_id])

                    query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = %s AND user_id = %s"
                    cursor.execute(query, tuple(values))
                    conn.commit()

                    if cursor.rowcount > 0:
                        return {"success": True, "message": "Tarea actualizada correctamente."}
                    else:
                        return {"error": "Tarea no encontrada o no pertenece al usuario."}

        except Exception as e:
            print("Error en update_task:", e)
            return {"error": str(e)}

        
        
    @staticmethod
    def delete_task(user_id, task_id):
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM tasks WHERE id = %s AND user_id = %s", 
                        (task_id, user_id)
                    )
                    conn.commit()
                    if cursor.rowcount > 0:
                        return {"success": True, "message": "Tarea eliminada correctamente."}
                    else:
                        return {"error": "Tarea no encontrada o no pertenece al usuario."}
                    
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def get_task(user_id, task_id):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT id, title, description, completed, created_at FROM tasks WHERE id = %s AND user_id = %s",
                        (task_id, user_id)
                    )
                    return cursor.fetchone()
        except Exception as e:
            return {"error": str(e)}
