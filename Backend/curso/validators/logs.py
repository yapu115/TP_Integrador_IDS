#Valida el post de logs
def validar_crear_log(data):
    errores = {}
    datos_validados = {}

    usuario_id = data.get("usuario_id")
    accion = data.get("accion")
    descripcion = data.get("descripcion")

    if usuario_id is not None:
        if not isinstance(usuario_id, int):
            errores["usuario_id"] = "El usuario_id debe ser un número entero."
        else:
            datos_validados["usuario_id"] = usuario_id

    if not accion:
        errores["accion"] = "La acción es obligatoria."
    elif not isinstance(accion, str):
        errores["accion"] = "La acción debe ser un texto."
    elif len(accion.strip()) > 50:
        errores["accion"] = "La acción no puede superar los 50 caracteres."
    else:
        datos_validados["accion"] = accion.strip().upper()

    if descripcion is not None:
        if not isinstance(descripcion, str):
            errores["descripcion"] = "La descripción debe ser un texto."
        elif len(descripcion.strip()) > 255:
            errores["descripcion"] = "La descripción no puede superar los 255 caracteres."
        else:
            datos_validados["descripcion"] = descripcion.strip()

    return errores, datos_validados