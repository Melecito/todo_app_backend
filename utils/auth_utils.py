import jwt
import datetime

SECRET_KEY = "clave_super_secreta_123"


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "user_id": payload["user_id"]}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "El token ha expirado."}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Token inválido"}