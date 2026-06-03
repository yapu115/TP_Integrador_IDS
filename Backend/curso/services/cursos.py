from curso.db import get_connection


def listar_cursos():
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, activo
            FROM cursos
            ORDER BY id;
        """
        cursor.execute(query)
        retorno = cursor.fetchall()
    except Exception as e:
        print(f"Error al listar cursos: {e}")
        retorno = None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return retorno


def obtener_curso(curso_id):
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, activo
            FROM cursos
            WHERE id = %s;
        """
        cursor.execute(query, (curso_id,))
        fila = cursor.fetchone()
        if fila is None:
            retorno = {"error": "NOT_FOUND", "mensaje": "Curso no encontrado."}
        else:
            retorno = fila
    except Exception as e:
        print(f"Error al obtener curso: {e}")
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return retorno


def crear_curso(data):
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = """
            INSERT INTO cursos (nombre, descripcion, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (
            data.get("nombre"),
            data.get("descripcion"),
            data.get("fecha_inicio"),
            data.get("fecha_fin"),
        ))
        conexion.commit()
        retorno = {"id": cursor.lastrowid}
    except Exception as e:
        print(f"Error al crear curso: {e}")
        if conexion: conexion.rollback()
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return retorno


def modificar_curso(curso_id, data):
    retorno = None
    conexion = None
    cursor = None
    try:
        check = obtener_curso(curso_id)
        if "error" in check:
            return check

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = """
            UPDATE cursos
            SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s, activo = %s
            WHERE id = %s;
        """
        cursor.execute(query, (
            data.get("nombre"),
            data.get("descripcion"),
            data.get("fecha_inicio"),
            data.get("fecha_fin"),
            data.get("activo", True),
            curso_id,
        ))
        conexion.commit()
        retorno = {"mensaje": "Curso modificado exitosamente."}
    except Exception as e:
        print(f"Error al modificar curso: {e}")
        if conexion: conexion.rollback()
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return retorno


def eliminar_curso(curso_id):
    retorno = None
    conexion = None
    cursor = None
    try:
        check = obtener_curso(curso_id)
        if "error" in check:
            return check

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("DELETE FROM cursos WHERE id = %s;", (curso_id,))
        conexion.commit()
        retorno = {"mensaje": "Curso eliminado exitosamente."}
    except Exception as e:
        print(f"Error al eliminar curso: {e}")
        if conexion: conexion.rollback()
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return retorno



def curso_existe(curso_id):
    conexion = None
    cursor = None
    existe = False
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM cursos WHERE id = %s;", (curso_id,))
        existe = cursor.fetchone() is not None
    except Exception:
        existe = False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return existe
