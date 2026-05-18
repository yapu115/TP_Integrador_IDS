from curso.db import get_connection
def listar_evaluaciones_service():
    conexion = None
    cursor = None
    try:
        conexion=get_connection()
        cursor=conexion.cursor(dictionary=True)
    
        query="SELECT * FROM tipos_evaluacion;"
        cursor.execute(query)
        resultado=cursor.fetchall()
    
        if len(resultado)<1:
            return None
        return resultado
    except Exception as e:
        print(f"Error al traer evaluaciones: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def crear_evaluacion_servicio(data):
    conexion=None
    cursor=None
    nombre = data["nombre"]
    descripcion = data["descripcion"]
    try:
        conexion=get_connection()
        cursor=conexion.cursor(dictionary=True)
    
        query="INSERT INTO tipos_evaluacion (nombre,descripcion) VALUES(%s,%s);"
        cursor.execute(query,(nombre,descripcion))
        conexion.commit()

        cambios=cursor.rowcount
        return cambios
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_evaluacion_service(id_evaluacion,data):
    conexion=None
    cursor=None
    nombre = data["nombre"]
    descripcion = data["descripcion"]
    try:
        conexion=get_connection()
        cursor=conexion.cursor(dictionary=True)
    
        query="UPDATE tipos_evaluacion SET nombre=%s,descripcion=%s WHERE id=%s;"
        cursor.execute(query,(nombre,descripcion,id_evaluacion))
        conexion.commit()

        cambios=cursor.rowcount
        return cambios
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def eliminar_evaluacion_service(id_evaluacion):
    conexion=None
    cursor=None
    try:
        conexion=get_connection()
        cursor=conexion.cursor(dictionary=True)
    
        query="DELETE FROM tipos_evaluacion WHERE id=%s;"
        cursor.execute(query,(id_evaluacion,))
        conexion.commit()

        cambios=cursor.rowcount
        return cambios
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()