from curso.db import get_connection

def ver_grupos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT grupos.id, grupos.nombre_grupo, grupo_evaluaciones.id_evaluacion as ids_tp, alumnos.id as alumno_id, alumnos.legajo, alumnos.nombre, alumnos.apellido
    FROM grupos
    LEFT JOIN grupo_evaluaciones ON grupos.id = grupo_evaluaciones.id_grupo
    LEFT JOIN grupo_integrantes ON grupos.id = grupo_integrantes.id_grupo
    LEFT JOIN alumnos ON alumnos.id = grupo_integrantes.id_alumno
    ORDER BY grupos.nombre_grupo;
    """
    cursor.execute(query)
    grupos = cursor.fetchall

    cursor.close()
    connection.close()

    return grupos

def agregar_grupo(nombre_grupo, ids_tp, integrantes):