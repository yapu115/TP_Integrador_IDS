from curso.db import get_connection

def ver_grupos():
    try:
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
    except Exception as e:
        return {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Error interno del servidor",
        "level": "error",
        "description": "Ocurrió un error inesperado. Por favor, intente más tarde."
        }

def crear_grupo(nombre_equipo, id_tp, ids_alumnos):
    try:
        if(not nombre_equipo or not id_tp or not ids_alumnos):
            return {
            "code": "VALIDATION_ERROR",
            "message": "El formato de los datos enviados es inválido.",
            "level": "error",
            "description": "Verifique que todos los campos requeridos estén presentes y tengan el formato correcto."
            }
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)


        query_grupos = """
        INSERT INTO equipos (nombre_equipo, id_tp)
        VALUES (%s,%d);
        """
        query_agregar_alumnos = """
        INSERT INTO equipos_integrantes (id_equipo, id_alumno)
        VALUES (%s,%s);
        """

        cursor.execute(query_grupos, (nombre_equipo, id_tp))
        connection.commit()
        id_equipo = cursor.lastrowid
        for id_alumno in ids_alumnos:
            cursor.execute(query_agregar_alumnos, (id_equipo, id_alumno))
        cursor.close()
        connection.close()
        
    except Exception as e:
        return {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Error interno del servidor",
        "level": "error",
        "description": "Ocurrió un error inesperado. Por favor, intente más tarde."
        }
    
def ver_grupo_id(id_grupo):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT equipos.id, equipos.nombre_equipo, equipos.ids_tp, alumnos.id, alumnos.legajo, alumnos.nombre, alumnos.apellido
        FROM ((equipos_integrantes
        JOIN equipos ON equipos.id=equipos_integrantes.id_equipo)
        LEFT JOIN alumnos ON alumnos.id=equipos_integrantes.id_alumno)
        WHERE equipos.id = %d;
        """
        cursor.execute(query, id_grupo)
        grupo = cursor.fetchone

        cursor.close()
        connection.close()

        return grupo
    except Exception as e:
        return {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Error interno del servidor",
        "level": "error",
        "description": "Ocurrió un error inesperado. Por favor, intente más tarde."
        }

def editar_grupo(id_grupo, valores):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    nombre_equipo = valores["nombre_equipo"]
    id_tp = = valores["id_tp"]
    id_alumno = valores["id_alumno"]

    query_equipos = """
    UPDATE equipos
    SET nombre_equipo = %s 
    WHERE id = %d;
    """
    query_tp ="""
    UPDATE equipos
    SET id_tp = %d
    WHERE id = %d
    """
    query_integrantes ="""
    UPDATE equipo_integrantes
    SET id_alumno = %d
    WHERE id_alumno = %d;
    """

    #Dependiendo del valor que se reciba para editar, se ejecuta un query distinto
    if(nombre_equipo):
        cursor.execute(query_equipos, ())
    else if(id_tp):
        cursor.execute(query,())
    else if(id_alumno):
        cursor.execute(query_integrantes, ())
    connection.commmit
    cambios = cursor.rowcount

    cursor.close()
    connection.close()

    return cambios
