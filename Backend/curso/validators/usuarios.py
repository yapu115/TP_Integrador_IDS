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


def validar_crear_usuario(data):
    """
    Verifica que al crear un usuario no falte ningún dato obligatorio,
    y que el correo electrónico tenga un formato válido.
    """
    errores = []
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    rol = data.get("rol")
    activo = data.get("activo", True)
    
    if not username:
        errores.append({
            "code": "VALIDATION_ERROR", 
            "message": "Falta el campo username.", 
            "description": "El nombre de usuario es obligatorio."
        })
    
    if not email:
        errores.append({
            "code": "VALIDATION_ERROR", 
            "message": "Falta el campo email.", 
            "description": "El correo electrónico es obligatorio."
        })

    # Exactamente un arroba y al menos un punto después de esta
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errores.append({
            "code": "VALIDATION_ERROR", 
            "message": "Formato de email inválido.", 
            "description": "Asegúrese de enviar un correo válido."
        })
        
    if not password:
        errores.append({
            "code": "VALIDATION_ERROR", 
            "message": "Falta el campo password.", 
            "description": "La contraseña es obligatoria al crear un usuario nuevo."
        })
        
    if not rol:
        errores.append({
            "code": "VALIDATION_ERROR", 
            "message": "Falta el campo rol.", 
            "description": "Debe especificar el rol del usuario."
        })
    elif rol not in ["admin", "profesor"]:
        errores.append({
            "code": "VALIDATION_ERROR", 
            "message": "Rol inválido.", 
            "description": "El rol solo puede ser 'admin' o 'profesor'."
        })
        
    return errores, {
        "username": username,
        "email": email,
        "password": password,
        "rol": rol,
        "activo": activo
    }
