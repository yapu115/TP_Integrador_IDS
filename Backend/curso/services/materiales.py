import os
from werkzeug.utils import secure_filename
from curso.db import get_connection

def listar_materiales():
    retorno = None
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT id, titulo, url_archivo, fecha_subida FROM materiales ORDER BY fecha_subida DESC"
    cursor.execute(query)
    materiales_db = cursor.fetchall()

    cursor.close()
    connection.close()

    materiales = []
    for m in materiales_db:
        fecha_str = m["fecha_subida"].strftime("%Y-%m-%dT%H:%M:%SZ") if hasattr(m["fecha_subida"], "strftime") else str(m["fecha_subida"])
        materiales.append({
            "id": m["id"],
            "titulo": m["titulo"],
            "url_archivo": m["url_archivo"],
            "fecha_subida": fecha_str
        })
        
    retorno = materiales
    return retorno


def guardar_material(titulo, archivo):
    retorno = None
    try:
        # El material se está guardando en local, pero tal vez sea mejor guardarlo en la nube, en algún otro lugar. 
        filename = secure_filename(archivo.filename) # Limpiar nombre del archivo para que sea seguro
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Carpeta /curso
        upload_folder = os.path.join(base_dir, "static", "materiales")
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
            
        file_path = os.path.join(upload_folder, filename)
        archivo.save(file_path)
        
        url_archivo = f"/static/materiales/{filename}"
        
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = "INSERT INTO materiales (titulo, url_archivo) VALUES (%s, %s)"
        cursor.execute(query, (titulo, url_archivo))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        retorno = {"mensaje": "Material subido exitosamente."}
    except Exception as e:
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
        
    return retorno


def eliminar_material(id_material):
    retorno = None
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    query_select = "SELECT url_archivo FROM materiales WHERE id = %s"
    cursor.execute(query_select, (id_material,))
    material = cursor.fetchone()
    
    if not material:
        cursor.close()
        connection.close()
        retorno = {"error": "NOT_FOUND", "mensaje": "Material no encontrado."}
    else:
        url_archivo = material["url_archivo"]
        
        query_delete = "DELETE FROM materiales WHERE id = %s"
        cursor.execute(query_delete, (id_material,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        filename = url_archivo.split("/")[-1]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "static", "materiales", filename)
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
            
        retorno = {"mensaje": "Material eliminado exitosamente."}
        
    return retorno
