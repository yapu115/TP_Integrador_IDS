from curso.db import get_connection

def listar_evaluaciones_service():
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT id, nombre, descripcion FROM tipos_evaluacion;"
        cursor.execute(query)
        resultado = cursor.fetchall()
    
        if len(resultado) < 1:
            retorno = []
        else:
            retorno = resultado
    except Exception as e:
        print(f"Error al traer evaluaciones: {e}")
        retorno = None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
            
    return retorno


def crear_evaluacion_servicio(data):
    retorno = None
    conexion = None
    cursor = None
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = "INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES (%s, %s);"
        cursor.execute(query, (nombre, descripcion))
        conexion.commit()
        retorno = cursor.rowcount
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        retorno = None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
            
    return retorno


def modificar_evaluacion_service(id_evaluacion, data):
    retorno = None
    conexion = None
    cursor = None
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = "UPDATE tipos_evaluacion SET nombre=%s, descripcion=%s WHERE id=%s;"
        cursor.execute(query, (nombre, descripcion, id_evaluacion))
        conexion.commit()
        retorno = cursor.rowcount
    except Exception as e:
        print(f"Error en BD: {e}")
        retorno = None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
            
    return retorno


def eliminar_evaluacion_service(id_evaluacion):
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = "DELETE FROM tipos_evaluacion WHERE id=%s;"
        cursor.execute(query, (id_evaluacion,))
        conexion.commit()
        retorno = cursor.rowcount
    except Exception as e:
        print(f"Error en BD: {e}")
        retorno = None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
            
    return retorno