from datetime import datetime, date


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validar_generar_qr(data):
    errores = []

    id_alumno = data.get("id_alumno")
    fecha = data.get("fecha")

    if not id_alumno:
        errores.append("El campo id_alumno es obligatorio.")

    try:
        id_alumno = int(id_alumno)
        if id_alumno <= 0:
            errores.append("El id_alumno debe ser mayor a 0.")
    except (ValueError, TypeError):
        errores.append("El id_alumno debe ser un número entero.")

    if not fecha:
        fecha = date.today().strftime("%Y-%m-%d")
    elif not validar_fecha(fecha):
        errores.append("La fecha debe tener formato YYYY-MM-DD.")

    return errores, {
        "id_alumno": id_alumno,
        "fecha": fecha
    }


def validar_registrar_asistencia(data):
    errores = []

    id_alumno = data.get("id_alumno")
    fecha = data.get("fecha")
    codigo_qr = data.get("codigo_qr")
    estado = data.get("estado", "presente")

    if not id_alumno:
        errores.append("El campo id_alumno es obligatorio.")

    try:
        id_alumno = int(id_alumno)
        if id_alumno <= 0:
            errores.append("El id_alumno debe ser mayor a 0.")
    except (ValueError, TypeError):
        errores.append("El id_alumno debe ser un número entero.")

    if not fecha:
        errores.append("El campo fecha es obligatorio.")
    elif not validar_fecha(fecha):
        errores.append("La fecha debe tener formato YYYY-MM-DD.")

    if not codigo_qr:
        errores.append("El campo codigo_qr es obligatorio.")

    estados_validos = ["presente", "ausente", "tarde"]

    if estado not in estados_validos:
        errores.append("El estado debe ser presente, ausente o tarde.")

    return errores, {
        "id_alumno": id_alumno,
        "fecha": fecha,
        "codigo_qr": codigo_qr,
        "estado": estado
    }