def validar_grupo(data):
    errores = []
    
    if not data:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Cuerpo de la petición vacío."
        })
    else:
        nombre = data.get("nombre")
        ids_tp = data.get("ids_tp")
        integrantes = data.get("integrantes")
        
        if not nombre or str(nombre).isspace():
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "Falta el campo nombre o está vacío."
            })
            
        if ids_tp is None or not isinstance(ids_tp, list):
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "El campo ids_tp debe ser una lista válida."
            })
            
        if integrantes is None or not isinstance(integrantes, list):
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "El campo integrantes debe ser una lista válida."
            })
            
    retorno = errores
    return retorno
