from curso.db import get_connection

def validar_campos_evaluaciones(data):
    errores = []
    
    if not data:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Cuerpo de la petición vacío."
        })
    else:
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")

        if not nombre or str(nombre).isspace():
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "Falta el campo nombre o está vacío."
            })

        if not descripcion or str(descripcion).isspace():
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "Falta el campo descripcion o está vacío."
            })

    retorno = errores
    return retorno
    
def validar_evaluacion(id_evaluacion):
    resultado = None
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        query = "SELECT id, nombre, descripcion FROM tipos_evaluacion WHERE id = %s;"
        cursor.execute(query, (id_evaluacion,))
        resultado = cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar evaluacion: {e}")
        resultado = None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close() 

    return resultado
