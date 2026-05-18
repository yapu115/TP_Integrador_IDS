from curso.db import get_connection
def validar_evaluaciones():
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
        print(f"Error al validar evaluaciones: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

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
    
    
