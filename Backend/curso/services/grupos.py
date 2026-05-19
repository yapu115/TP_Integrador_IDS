from curso.db import get_connection

def ver_grupos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT equipos.id, equipos.nombre_equipo, equipos.ids_tp, alumnos.id, alumnos.legajo, alumnos.nombre, alumnos.apellido
    FROM ((equipos_integrantes
    JOIN equipos ON equipos.id=equipos_integrantes.id_equipo)
    LEFT JOIN alumnos ON alumnos.id=equipos_integrantes.id_alumno)
    ORDER BY equipos.nombre_equipo;
    """
    cursor.execute(query)
    grupos = cursor.fetchall

    cursor.close()
    connection.close()

    return grupos

def agregar_grupo(nombre_grupo, ids_tp, integrantes):