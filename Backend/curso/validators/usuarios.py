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
            "message": "Falta el campo usuario.",
            "description": "El nombre de usuario es requerido para iniciar sesión."
        })

    if not password:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo contraseña.",
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


def validar_actualizar_usuario(data):
    """
    Verifica que al actualizar un usuario, los datos proporcionados sean válidos.
    Todos los campos son opcionales.
    """
    errores = []
    datos_validados = {}
    
    if "username" in data:
        if not data["username"]:
            errores.append({"code": "VALIDATION_ERROR", "message": "El username no puede estar vacío."})
        else:
            datos_validados["username"] = data["username"]
            
    if "email" in data:
        email = data["email"]
        if not email:
            errores.append({"code": "VALIDATION_ERROR", "message": "El email no puede estar vacío."})
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errores.append({"code": "VALIDATION_ERROR", "message": "Formato de email inválido."})
        else:
            datos_validados["email"] = email
            
    if "password" in data:
        if not data["password"]:
            errores.append({"code": "VALIDATION_ERROR", "message": "La contraseña no puede estar vacía."})
        else:
            datos_validados["password"] = data["password"]
            
    if "rol" in data:
        rol = data["rol"]
        if rol not in ["admin", "profesor"]:
            errores.append({"code": "VALIDATION_ERROR", "message": "Rol inválido. Solo puede ser 'admin' o 'profesor'."})
        else:
            datos_validados["rol"] = rol
            
    if "activo" in data:
        if not isinstance(data["activo"], bool):
            errores.append({"code": "VALIDATION_ERROR", "message": "El campo activo debe ser booleano (True/False)."})
        else:
            datos_validados["activo"] = data["activo"]
            
    if not datos_validados and not errores:
        errores.append({"code": "VALIDATION_ERROR", "message": "Debe proporcionar al menos un campo para actualizar."})
        
    return errores, datos_validados
