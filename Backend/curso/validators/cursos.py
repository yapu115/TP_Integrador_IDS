def validar_curso(data):
    errores = []

    nombre = data.get("nombre")
    if not nombre or str(nombre).strip() == "":
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El campo 'nombre' es obligatorio."
        })
    elif len(str(nombre).strip()) > 100:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El campo 'nombre' no puede superar los 100 caracteres."
        })

    fecha_inicio = data.get("fecha_inicio")
    fecha_fin    = data.get("fecha_fin")

    if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "La fecha de fin no puede ser anterior a la fecha de inicio."
        })

    return errores
