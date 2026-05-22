# Valida el post de logs
def validar_crear_log(data):
    errores = []
    datos_validados = {}

    id_usuario = data.get("id_usuario")
    if id_usuario is None and "usuario" in data:
        id_usuario = data.get("usuario")

    accion = data.get("accion")
    detalles = data.get("detalles")

    if id_usuario is not None:
        try:
            datos_validados["id_usuario"] = int(id_usuario)
        except (TypeError, ValueError):
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "El id_usuario debe ser un número entero.",
                "level": "error",
            })

    if not accion:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "La acción es obligatoria.",
            "level": "error",
        })
    elif not isinstance(accion, str):
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "La acción debe ser un texto.",
            "level": "error",
        })
    elif len(accion.strip()) > 255:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "La acción no puede superar los 255 caracteres.",
            "level": "error",
        })
    else:
        datos_validados["accion"] = accion.strip()

    if detalles is not None:
        if not isinstance(detalles, str):
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "Los detalles deben ser un texto.",
                "level": "error",
            })
        else:
            datos_validados["detalles"] = detalles.strip()

    return errores, datos_validados if not errores else None
