def validar_notas(data):
    """
    Verifica que al registrar o actualizar una nota no falte la info requerida.
    """
    errores = []

    id_alumno = data.get("id_alumno")
    id_evaluacion = data.get("id_evaluacion")
    nota = data.get("nota")

    if id_alumno is None:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El formato de los datos enviados es inválido.",
            "level": "error",
            "description": "La id del alumno es un campo requerido para enviar una solicitud."
        })

    if id_evaluacion is None:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El formato de los datos enviados es inválido.",
            "level": "error",
            "description": "La id de la evaluacion es un campo requerido para enviar una solicitud."
        })

    if nota is None:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El formato de los datos enviados es inválido.",
            "level": "error",
            "description": "La nota es un campo requerido para enviar una solicitud."
        })

    return errores