from flask_jwt_extended import create_access_token

def generate_token(user_id):
    """
    Genera un token JWT compatible con Flask-JWT-Extended.
    """
    return create_access_token(identity=str(user_id))
