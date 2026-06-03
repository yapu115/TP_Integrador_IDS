from curso.db import get_connection


def _agrupar_resultados(filas):
    grupos_dict = {}
    for f in filas:
        id_g = f["id"]
        if id_g not in grupos_dict:
            grupos_dict[id_g] = {
                "id_grupo":    id_g,
                "nombre":      f["nombre_grupo"],
                "curso_id":    f["curso_id"],
                "ids_tp":      set(),
                "integrantes": set()
            }
        if f["id_evaluacion"]:
            grupos_dict[id_g]["ids_tp"].add(f["id_evaluacion"])
        if f["id_alumno"]:
            grupos_dict[id_g]["integrantes"].add(f["id_alumno"])

    for g in grupos_dict.values():
        g["ids_tp"]      = list(g["ids_tp"])
        g["integrantes"] = list(g["integrantes"])

    return list(grupos_dict.values())


def listar_grupos(curso_id):
    retorno  = None
    conexion = None
    cursor   = None
    try:
        conexion = get_connection()
        cursor   = conexion.cursor(dictionary=True)
        query = """
            SELECT g.id, g.nombre_grupo, g.curso_id,
                   ge.id_evaluacion, gi.id_alumno
            FROM grupos g
            LEFT JOIN grupo_evaluaciones ge ON g.id = ge.id_grupo
            LEFT JOIN grupo_integrantes  gi ON g.id = gi.id_grupo
            WHERE g.curso_id = %s
            ORDER BY g.nombre_grupo;
        """
        cursor.execute(query, (curso_id,))
        filas   = cursor.fetchall()
        retorno = _agrupar_resultados(filas)
    except Exception as e:
        print(f"Error al listar grupos: {e}")
        retorno = None
    finally:
        if cursor:  cursor.close()
        if conexion: conexion.close()
    return retorno



def obtener_grupo(id_grupo):
    retorno  = None
    conexion = None
    cursor   = None
    try:
        conexion = get_connection()
        cursor   = conexion.cursor(dictionary=True)
        query = """
            SELECT g.id, g.nombre_grupo, g.curso_id,
                   ge.id_evaluacion, gi.id_alumno
            FROM grupos g
            LEFT JOIN grupo_evaluaciones ge ON g.id = ge.id_grupo
            LEFT JOIN grupo_integrantes  gi ON g.id = gi.id_grupo
            WHERE g.id = %s;
        """
        cursor.execute(query, (id_grupo,))
        filas = cursor.fetchall()
        if not filas:
            retorno = {"error": "NOT_FOUND", "mensaje": "Grupo no encontrado."}
        else:
            grupos  = _agrupar_resultados(filas)
            retorno = grupos[0] if grupos else None
    except Exception as e:
        print(f"Error al obtener grupo: {e}")
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor:  cursor.close()
        if conexion: conexion.close()
    return retorno


def crear_grupo(data, curso_id):
    retorno  = None
    conexion = None
    cursor   = None
    nombre      = data.get("nombre")
    ids_tp      = data.get("ids_tp", [])
    integrantes = data.get("integrantes", [])
    try:
        conexion = get_connection()
        cursor   = conexion.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO grupos (nombre_grupo, curso_id) VALUES (%s, %s);",
            (nombre, curso_id)
        )
        id_grupo = cursor.lastrowid

        if ids_tp:
            for id_tp in ids_tp:
                cursor.execute(
                    "INSERT INTO grupo_evaluaciones (id_grupo, id_evaluacion) VALUES (%s, %s);",
                    (id_grupo, id_tp)
                )
        if integrantes:
            for id_alumno in integrantes:
                cursor.execute(
                    "INSERT INTO grupo_integrantes (id_grupo, id_alumno) VALUES (%s, %s);",
                    (id_grupo, id_alumno)
                )

        conexion.commit()
        retorno = {"id_grupo": id_grupo}
    except Exception as e:
        if conexion: conexion.rollback()
        if "foreign key constraint" in str(e).lower():
            retorno = {"error": "VALIDATION_ERROR", "mensaje": "Algún alumno o evaluación indicado no existe."}
        else:
            print(f"Error al crear grupo: {e}")
            retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor:  cursor.close()
        if conexion: conexion.close()
    return retorno


def modificar_grupo(id_grupo, data):
    retorno  = None
    conexion = None
    cursor   = None
    nombre      = data.get("nombre")
    ids_tp      = data.get("ids_tp", [])
    integrantes = data.get("integrantes", [])
    try:
        check = obtener_grupo(id_grupo)
        if check and "error" in check:
            return check

        conexion = get_connection()
        cursor   = conexion.cursor(dictionary=True)

        cursor.execute("UPDATE grupos SET nombre_grupo = %s WHERE id = %s;", (nombre, id_grupo))
        cursor.execute("DELETE FROM grupo_evaluaciones WHERE id_grupo = %s", (id_grupo,))
        cursor.execute("DELETE FROM grupo_integrantes  WHERE id_grupo = %s", (id_grupo,))

        for id_tp in ids_tp:
            cursor.execute(
                "INSERT INTO grupo_evaluaciones (id_grupo, id_evaluacion) VALUES (%s, %s);",
                (id_grupo, id_tp)
            )
        for id_alumno in integrantes:
            cursor.execute(
                "INSERT INTO grupo_integrantes (id_grupo, id_alumno) VALUES (%s, %s);",
                (id_grupo, id_alumno)
            )

        conexion.commit()
        retorno = {"mensaje": "Grupo modificado con éxito."}
    except Exception as e:
        print(f"Error al modificar grupo: {e}")
        if conexion: conexion.rollback()
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor:  cursor.close()
        if conexion: conexion.close()
    return retorno



def eliminar_grupo(id_grupo):
    retorno  = None
    conexion = None
    cursor   = None
    try:
        check = obtener_grupo(id_grupo)
        if check and "error" in check:
            return check

        conexion = get_connection()
        cursor   = conexion.cursor(dictionary=True)
        cursor.execute("DELETE FROM grupos WHERE id = %s;", (id_grupo,))
        conexion.commit()
        retorno = {"mensaje": "Grupo eliminado."}
    except Exception as e:
        print(f"Error al eliminar grupo: {e}")
        if conexion: conexion.rollback()
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor:  cursor.close()
        if conexion: conexion.close()
    return retorno
