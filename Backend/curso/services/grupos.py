from curso.db import get_connection

def _agrupar_resultados(filas):
    grupos_dict = {}
    for f in filas:
        id_g = f["id"]
        if id_g not in grupos_dict:
            grupos_dict[id_g] = {
                "id_grupo": id_g,
                "nombre": f["nombre_grupo"],
                "ids_tp": set(),
                "integrantes": set()
            }
        
        if f["id_evaluacion"]:
            grupos_dict[id_g]["ids_tp"].add(f["id_evaluacion"])
        if f["id_alumno"]:
            grupos_dict[id_g]["integrantes"].add(f["id_alumno"])
            
    for g in grupos_dict.values():
        g["ids_tp"] = list(g["ids_tp"])
        g["integrantes"] = list(g["integrantes"])
        
    return list(grupos_dict.values())

def listar_grupos():
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        query = """
        SELECT g.id, g.nombre_grupo, ge.id_evaluacion, gi.id_alumno
        FROM grupos g
        LEFT JOIN grupo_evaluaciones ge ON g.id = ge.id_grupo
        LEFT JOIN grupo_integrantes gi ON g.id = gi.id_grupo
        ORDER BY g.nombre_grupo;
        """
        cursor.execute(query)
        filas = cursor.fetchall()
        
        retorno = _agrupar_resultados(filas)
    except Exception as e:
        print(f"Error al listar grupos: {e}")
        retorno = None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
        
    return retorno

def obtener_grupo(id_grupo):
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        query = """
        SELECT g.id, g.nombre_grupo, ge.id_evaluacion, gi.id_alumno
        FROM grupos g
        LEFT JOIN grupo_evaluaciones ge ON g.id = ge.id_grupo
        LEFT JOIN grupo_integrantes gi ON g.id = gi.id_grupo
        WHERE g.id = %s;
        """
        cursor.execute(query, (id_grupo,))
        filas = cursor.fetchall()
        
        if not filas:
            retorno = {"error": "NOT_FOUND", "mensaje": "Grupo no encontrado."}
        else:
            grupos = _agrupar_resultados(filas)
            retorno = grupos[0] if grupos else None
    except Exception as e:
        print(f"Error al obtener grupo: {e}")
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
        
    return retorno

def crear_grupo(data):
    retorno = None
    conexion = None
    cursor = None
    nombre = data.get("nombre")
    ids_tp = data.get("ids_tp", [])
    integrantes = data.get("integrantes", [])
    
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        query_grupos = "INSERT INTO grupos (nombre_grupo) VALUES (%s);"
        cursor.execute(query_grupos, (nombre,))
        id_grupo = cursor.lastrowid
        
        if ids_tp:
            query_tps = "INSERT INTO grupo_evaluaciones (id_grupo, id_evaluacion) VALUES (%s, %s);"
            for id_tp in ids_tp:
                cursor.execute(query_tps, (id_grupo, id_tp))
                
        if integrantes:
            query_integrantes = "INSERT INTO grupo_integrantes (id_grupo, id_alumno) VALUES (%s, %s);"
            for id_alumno in integrantes:
                cursor.execute(query_integrantes, (id_grupo, id_alumno))
                
        conexion.commit()
        retorno = {"id_grupo": id_grupo}

    except Exception as e:
        if "foreign key constraint" in str(e):
            retorno = {"error": "VALIDATION_ERROR",
                    "mensaje": "Algún alumno indicado no existe."}
        else:
            print(f"Error al crear grupo: {e}")
            if conexion: conexion.rollback()
            retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
        
    return retorno
    
def modificar_grupo(id_grupo, data):
    retorno = None
    conexion = None
    cursor = None
    nombre = data.get("nombre")
    ids_tp = data.get("ids_tp", [])
    integrantes = data.get("integrantes", [])
    
    try:
        check = obtener_grupo(id_grupo)
        if check and "error" in check:
            retorno = check
        else:
            conexion = get_connection()
            cursor = conexion.cursor(dictionary=True)

            query_update = "UPDATE grupos SET nombre_grupo = %s WHERE id = %s;"
            cursor.execute(query_update, (nombre, id_grupo))
            
            cursor.execute("DELETE FROM grupo_evaluaciones WHERE id_grupo = %s", (id_grupo,))
            cursor.execute("DELETE FROM grupo_integrantes WHERE id_grupo = %s", (id_grupo,))
            
            query_tps = "INSERT INTO grupo_evaluaciones (id_grupo, id_evaluacion) VALUES (%s, %s);"
            for id_tp in ids_tp:
                cursor.execute(query_tps, (id_grupo, id_tp))
                
            query_integrantes = "INSERT INTO grupo_integrantes (id_grupo, id_alumno) VALUES (%s, %s);"
            for id_alumno in integrantes:
                cursor.execute(query_integrantes, (id_grupo, id_alumno))
                
            conexion.commit()
            retorno = {"mensaje": "Grupo modificado con éxito."}
    except Exception as e:
        print(f"Error al modificar grupo: {e}")
        if conexion: conexion.rollback()
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
        
    return retorno
    
def eliminar_grupo(id_grupo):
    retorno = None
    conexion = None
    cursor = None
    try:
        check = obtener_grupo(id_grupo)
        if check and "error" in check:
            retorno = check
        else:
            conexion = get_connection()
            cursor = conexion.cursor(dictionary=True)
            
            query = "DELETE FROM grupos WHERE id = %s;"
            cursor.execute(query, (id_grupo,))
            conexion.commit()
            
            retorno = {"mensaje": "Grupo eliminado."}
    except Exception as e:
        print(f"Error al eliminar grupo: {e}")
        if conexion: conexion.rollback()
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
        
    return retorno
