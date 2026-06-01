def validar_subida_material(data):
    errores = []
    
    titulo = data.get("titulo")
    url_archivo = data.get("url_archivo")

    if not titulo or not titulo.strip():
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo titulo.",
            "description": "El título del material es obligatorio."
        })

    if not url_archivo or not url_archivo.strip():
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo url_archivo.",
            "description": "Debe adjuntar una URL para el material."
        })
        
    retorno = (errores, {
        "titulo": titulo.strip() if titulo else None,
        "url_archivo": url_archivo.strip() if url_archivo else None
    })
    
    return retorno
