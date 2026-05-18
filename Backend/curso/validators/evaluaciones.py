from curso.db import get_connection

def validar_campos_evaluaciones(data):
    nombre = data["nombre"]
    descripcion = data["descripcion"]
    campos_validos=True
    if not data or "nombre" not in data or "descripcion" not in data:
        campos_validos=False
    if not nombre or nombre.isspace():
        campos_validos=False

    if not descripcion or descripcion.isspace():
        campos_validos=False
    return campos_validos
    
def validar_evaluacion(id_evaluacion):
    conexion = None
    cursor = None
    try:
        conexion=get_connection()
        cursor=conexion.cursor(dictionary=True)

        query="SELECT nombre, descripcion FROM tipos_evaluacion WHERE id = %s;"
        cursor.execute(query,(id_evaluacion,))
        resultado=cursor.fetchone()

        return resultado
    except Exception as e:
        print(f"Error al buscar evaluacion: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close() 
