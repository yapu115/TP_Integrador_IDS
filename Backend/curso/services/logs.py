from curso.db import get_connection

_QUERY_BASE = """
    SELECT
        l.id,
        l.id_usuario,
        u.username AS usuario,
        l.accion,
        l.fecha,
        l.detalles
    FROM logs_actividad l
    LEFT JOIN usuarios u ON l.id_usuario = u.id
"""


def formatear_log(fila):
    if not fila:
        return None
    return {
        "id": fila["id"],
        "usuario": fila["usuario"],
        "accion": fila["accion"],
        "fecha": fila["fecha"],
        "detalles": fila["detalles"],
    }


def obtener_log_por_id(id_log):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = _QUERY_BASE + " WHERE l.id = %s"
        cursor.execute(query, (id_log,))
        return formatear_log(cursor.fetchone())
    finally:
        cursor.close()
        connection.close()


def crear_log(datos):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            INSERT INTO logs_actividad (id_usuario, accion, detalles)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            datos.get("id_usuario"),
            datos["accion"],
            datos.get("detalles"),
        ))
        connection.commit()
        id_log = cursor.lastrowid
    finally:
        cursor.close()
        connection.close()

    return obtener_log_por_id(id_log)


def listar_logs(usuario_id=None, accion=None, fecha=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = _QUERY_BASE + " WHERE 1=1"
        params = []

        if usuario_id:
            query += " AND l.id_usuario = %s"
            params.append(usuario_id)

        if accion:
            query += " AND l.accion = %s"
            params.append(accion)

        if fecha:
            query += " AND DATE(l.fecha) = %s"
            params.append(fecha)

        query += " ORDER BY l.fecha DESC"
        cursor.execute(query, tuple(params))
        logs = [formatear_log(fila) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()

    return {"logs": logs}
