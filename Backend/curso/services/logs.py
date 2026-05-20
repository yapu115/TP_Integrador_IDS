from curso.db import get_connection

def obtener_log_por_id(id_log):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM logs WHERE id_log = %s"
    cursor.execute(query, (id_log,))

    log = cursor.fetchone()

    cursor.close()
    connection.close()

    return log


def crear_log(datos):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        INSERT INTO logs (usuario_id, accion, descripcion)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (
        datos.get("usuario_id"),
        datos["accion"],
        datos.get("descripcion")
    ))

    connection.commit()

    id_log = cursor.lastrowid



def listar_logs(usuario_id=None, accion=None, fecha=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM logs WHERE 1=1" #El where significa que es siempre verdadera
    params = []

    if usuario_id:
        query += " AND usuario_id = %s"
        params.append(usuario_id)

    if accion:
        query += " AND accion = %s"
        params.append(accion)

    if fecha:
        query += " AND DATE(fecha_hora) = %s"
        params.append(fecha)

    cursor.execute(query, tuple(params))

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return logs