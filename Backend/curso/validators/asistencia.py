from datetime import datetime, date


def validar_fecha(fecha):
    es_valida = False
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        es_valida = True
    except ValueError:
        pass
    return es_valida


def validar_generar_qr(data):
    errores = []

    fecha = data.get("fecha")

    if not fecha:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo fecha.",
            "description": "Debe especificar una fecha para generar el QR de la clase."
        })
    elif not validar_fecha(fecha):
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Formato de fecha inválido.",
            "description": "La fecha debe tener formato YYYY-MM-DD."
        })

    return errores, {
        "fecha": fecha
    }


def validar_enviar_qr(data):
    errores = []

    id_alumno = data.get("id_alumno")
    fecha = data.get("fecha")

    if not id_alumno:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo id_alumno.",
            "description": "Debe especificar a qué alumno enviar el QR."
        })
    else:
        try:
            id_alumno = int(id_alumno)
            if id_alumno <= 0:
                errores.append({
                    "code": "VALIDATION_ERROR",
                    "message": "El id_alumno debe ser mayor a 0.",
                    "description": "El id_alumno debe ser un entero positivo."
                })
        except (ValueError, TypeError):
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "El id_alumno debe ser un número entero.",
                "description": "Tipo de dato incorrecto para id_alumno."
            })

    if not fecha:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo fecha.",
            "description": "Debe especificar una fecha para el QR del alumno."
        })
    elif not validar_fecha(fecha):
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Formato de fecha inválido.",
            "description": "La fecha debe tener formato YYYY-MM-DD."
        })

    return errores, {
        "id_alumno": id_alumno,
        "fecha": fecha
    }


def validar_registrar_asistencia(data):
    errores = []

    codigo_qr = data.get("codigo_qr")

    if not codigo_qr:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo codigo_qr.",
            "description": "Debe proporcionar el texto del código QR escaneado."
        })

    return errores, {
        "codigo_qr": codigo_qr
    }