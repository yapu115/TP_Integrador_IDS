import jwt
import os
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '11501284827B383944290E9348723R483E')

def token_required(f):
    """
    Decorador para proteger rutas que requieren autenticación JWT.
    Verifica que el header Authorization contenga un Bearer token válido.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({
                "errors": [
                    {
                        "code": "UNAUTHORIZED",
                        "message": "Token de autenticación faltante.",
                        "level": "error",
                        "description": "Se requiere un token JWT válido en el header Authorization."
                    }
                ]
            }), 401
            
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.usuario_actual = data
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                "errors": [
                    {
                        "code": "TOKEN_EXPIRED",
                        "message": "El token ha expirado.",
                        "level": "error",
                        "description": "Por favor, inicie sesión nuevamente para obtener un nuevo token."
                    }
                ]
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "errors": [
                    {
                        "code": "INVALID_TOKEN",
                        "message": "Token inválido.",
                        "level": "error",
                        "description": "El token proporcionado no es válido o está corrupto."
                    }
                ]
            }), 401
            
        return f(*args, **kwargs)
    
    return decorated
