#Valida el post de logs
def validar_crear_log(data):
    errores = {}
    datos_validados = {}

    usuario = data.get("usuario")
    accion = data.get("accion")
    detalles = data.get("detalles")

    if usuario:
        if not isinstance(usuario, str):
            errores["usuario"] = "El usuario debe ser un número entero."
        else:
            datos_validados["usuario"] = usuario

    if not accion:
        errores["accion"] = "La acción es obligatoria."
    elif not isinstance(accion, str):
        errores["accion"] = "La acción debe ser un texto."
    elif len(accion.strip()) > 50:
        errores["accion"] = "La acción no puede superar los 50 caracteres."
    else:
        datos_validados["accion"] = accion.strip().upper()

    if detalles is not None:
        if not isinstance(detalles, str):
            errores["detalles"] = "La descripción debe ser un texto."
        elif len(detalles.strip()) > 255:
            errores["detalles"] = "La descripción no puede superar los 255 caracteres."
        else:
            datos_validados["detalles"] = detalles.strip()

    return errores, datos_validados