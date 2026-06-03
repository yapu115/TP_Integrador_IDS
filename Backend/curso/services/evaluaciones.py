from curso.db import get_connection

def listar_evaluaciones_service():
    retorno = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM tipos_evaluacion;"
        cursor.execute(query)
        resultado = cursor.fetchall()
    
        if len(resultado) < 1:
            retorno = []
        else:
            for evaluacion in resultado:
                evaluacion["hora"] = str(evaluacion["hora"])
                evaluacion["fecha"] = str(evaluacion["fecha"])
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
    fecha=data.get("fecha")
    hora=data.get("hora")
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = "INSERT INTO tipos_evaluacion (nombre, descripcion, fecha, hora) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (nombre, descripcion, fecha, hora))
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
    fecha=data.get("fecha")
    hora=data.get("hora")
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        query = "UPDATE tipos_evaluacion SET nombre=%s, descripcion=%s, fecha=%s, hora=%s WHERE id=%s;"
        cursor.execute(query, (nombre, descripcion, fecha, hora, id_evaluacion))
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