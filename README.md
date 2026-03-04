# Todo App Backend

API REST desarrollada con Flask, MySQL y JWT para gestión de usuarios y tareas.

## 🚀 Tecnologías
- Python
- Flask
- MySQL
- Docker
- JWT (flask-jwt-extended)

## ⚙️ Variables de entorno

Crear archivo `.env`:

DB_HOST=mysql_db
DB_USER=root
DB_PASS=tu_password
DB_NAME=todo_app
DB_PORT=3306
JWT_SECRET=tu_clave_secreta

## 🐳 Ejecutar con Docker

docker compose up --build

Backend disponible en:
http://localhost:8000/api

## 🔐 Autenticación

POST /api/login  
Header:
Authorization: Bearer TOKEN

## 📌 Endpoints

GET /api/users  
GET /api/users/<id>  
POST /api/users  
PUT /api/users/<id>  
DELETE /api/users/<id>  
POST /api/login