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

def crear_grupo(nombre_equipo, id_tp, ids_alumnos):
    """
    Falta verificacion y manejo de errores.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query_grupos = """
    INSERT INTO equipos (nombre_equipo, id_tp)
    VALUES (%s,%d);
    """
    query_alumnos = """
    INSERT INTO equipos_integrantes (id_equipo, id_alumno)
    VALUES (%s,%s);
    """

    cursor.execute(query_grupos, (nombre_equipo, id_tp))
    connection.commit()
    id_equipo = cursor.lastrowid
    for id_alumno in ids_alumnos:
        cursor.execute(query_alumnos, (id_equipo, id_alumno))
    cursor.close()
    connection.close()


