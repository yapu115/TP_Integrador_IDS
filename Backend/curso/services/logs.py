from curso.db import get_connection

def obtener_log_por_id(id_log):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM logs_actividad WHERE id = %s"
    cursor.execute(query, (id_log,))

    log = cursor.fetchone()

    cursor.close()
    connection.close()

    return log


def crear_log(datos):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        INSERT INTO logs_actividad (usuario, accion, detalles)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (
        datos.get("usuario"),
        datos["accion"],
        datos.get("detalles")
    ))

    connection.commit()

    id_log = cursor.lastrowid



def listar_logs(usuario=None, accion=None, fecha=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM logs_actividad WHERE 1=1" #El where significa que es siempre verdadera
    params = []

    if usuario:
        query += " AND usuario = %s"
        params.append(usuario)

    if accion:
        query += " AND accion = %s"
        params.append(accion)

    if fecha:
        query += " AND DATE(fecha) = %s"
        params.append(fecha)

    cursor.execute(query, tuple(params))

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return logs