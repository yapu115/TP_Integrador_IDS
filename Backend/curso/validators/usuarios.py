import re

def validar_login(data):
    """
    Verifica que el usuario haya enviado su username y password
    al intentar iniciar sesión.
    """
    errores = []
    
    username = data.get("username")
    password = data.get("password")
    
    if not username:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo username.",
            "description": "El nombre de usuario es requerido para iniciar sesión."
        })
        
    if not password:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo password.",
            "description": "La contraseña es requerida para iniciar sesión."
        })
        
    return errores, {
        "username": username,
        "password": password
    }


