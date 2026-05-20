def validar_subida_material(data):
    errores = []
    
    titulo = data.get("titulo")
    archivo = data.get("file")

    if not titulo or not titulo.strip():
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo titulo.",
            "description": "El título del material es obligatorio."
        })

    if not archivo or not archivo.filename:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo file.",
            "description": "Debe adjuntar un archivo físico para subir."
        })
        
    retorno = (errores, {
        "titulo": titulo.strip() if titulo else None,
        "file": archivo
    })
    
    return retorno
