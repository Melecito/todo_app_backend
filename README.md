# Todo App Backend

API REST robusta desarrollada con Flask, MySQL y JWT para la gestión eficiente de usuarios y tareas. Este proyecto está completamente contenerizado con Docker, facilitando su despliegue en cualquier entorno.

---

## Tecnologías Utilizadas

- Lenguaje: Python 3.11
- Framework: Flask
- Base de Datos: MySQL 8
- Infraestructura: Docker & Docker Compose
- Seguridad: Flask-JWT-Extended & Bcrypt (Hashing de contraseñas) 

---

## Configuración del Entorno

Para que la aplicación funcione correctamente, crea un archivo .env en la raíz del proyecto con las siguientes variables:

DB_HOST=mysql_db
DB_USER=root
DB_PASS=tu_password
DB_NAME=todo_app
DB_PORT=3306
JWT_SECRET=tu_clave_secreta_super_segura


---

## Despliegue con Docker

Ejecuta el siguiente comando para levantar los servicios (API y Base de Datos):


docker compose up --build

La API estará disponible en:

http://localhost:8000/api


---

## Autenticación y Seguridad

La API utiliza JSON Web Tokens (JWT). Para acceder a las rutas protegidas, debes incluir el token en el header de tus peticiones:

Header: Authorization: Bearer <TU_TOKEN>

Login
POST /api/login

Body (JSON):


json
{
  "email": "user@mail.com",
  "password": "123456"
}


| Método | Endpoint | Descripción | Protegido |
| :--- | :--- | :--- | :---: |
| **POST** | `/api/login` | Iniciar sesión y obtener token | ❌ |
| **GET** | `/api/users` | Listar todos los usuarios | ✅ |
| **GET** | `/api/users/<id>` | Obtener detalle de un usuario | ✅ |
| **POST** | `/api/users` | Registrar un nuevo usuario | ❌ |
| **PUT** | `/api/users/<id>` | Actualizar información de usuario | ✅ |
| **DELETE** | `/api/users/<id>` | Eliminar un usuario | ✅ |



## Estructura del Proyecto

```text
.
├── controllers/          # Lógica de negocio
├── models/               # Definición de tablas y esquemas
├── sql/                  # Scripts de inicialización de DB
├── utils/                # Funciones auxiliares y decoradores
├── app.py                # Punto de entrada de la aplicación
├── routes.py             # Definición de rutas
├── db_config.py          # Configuración de conexión MySQL
├── docker-compose.yml    # Orquestación de contenedores
├── Dockerfile            # Configuración de imagen Docker
└── requirements.txt      # Dependencias de Python




