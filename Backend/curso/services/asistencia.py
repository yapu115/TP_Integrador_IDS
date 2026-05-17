from curso.db import get_connection


# Genera un código QR simulado para pruebas del sistema.
# Actualmente no crea imágenes QR reales.
def generar_codigo_qr(id_alumno, fecha):
    # En un escenario real, aquí se generaría un código QR utilizando una biblioteca como qrcode.
    return f"ASISTENCIA-{id_alumno}-{fecha}"


def alumno_existe(id_alumno):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id
        FROM alumnos
        WHERE id = %s
    """

    cursor.execute(query, (id_alumno,))
    alumno = cursor.fetchone()

    cursor.close()
    connection.close()

    return alumno is not None


def generar_qr_asistencia(id_alumno, fecha):
    if not alumno_existe(id_alumno):
        return None

    codigo_qr = generar_codigo_qr(id_alumno, fecha)

    return {
        "id_alumno": id_alumno,
        "fecha": fecha,
        "codigo_qr": codigo_qr,
        "mensaje": "Código QR simulado generado correctamente."
    }

# Registra asistencia del alumno.
# Si ya existe asistencia para esa fecha, actualiza el registro.
def registrar_asistencia(id_alumno, fecha, codigo_qr, estado):
    if not alumno_existe(id_alumno):
        return {
            "ok": False,
            "status": 404,
            "mensaje": "No existe un alumno con ese id."
        }

    codigo_esperado = generar_codigo_qr(id_alumno, fecha)

    if codigo_qr != codigo_esperado:
        return {
            "ok": False,
            "status": 400,
            "mensaje": "El código QR no corresponde al alumno o a la fecha."
        }

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        INSERT INTO asistencias (id_alumno, fecha, estado, codigo_qr)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            estado = VALUES(estado),
            codigo_qr = VALUES(codigo_qr)
    """

    cursor.execute(query, (id_alumno, fecha, estado, codigo_qr))
    connection.commit()

    cursor.close()
    connection.close()

    return {
        "ok": True,
        "status": 201,
        "mensaje": "Asistencia registrada correctamente.",
        "data": {
            "id_alumno": id_alumno,
            "fecha": fecha,
            "estado": estado,
            "codigo_qr": codigo_qr
        }
    }

# Obtiene historial completo de asistencias de un alumno.
def obtener_asistencias_por_alumno(id_alumno):
    if not alumno_existe(id_alumno):
        return None

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            id_asistencia,
            id_alumno,
            fecha,
            estado,
            codigo_qr,
            creado_en
        FROM asistencias
        WHERE id_alumno = %s
        ORDER BY fecha DESC
    """

    cursor.execute(query, (id_alumno,))
    asistencias = cursor.fetchall()

    cursor.close()
    connection.close()

    return asistencias