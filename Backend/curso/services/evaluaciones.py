from curso.db import get_connection

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