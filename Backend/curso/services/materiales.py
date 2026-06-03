import os
from werkzeug.utils import secure_filename
from curso.db import get_connection


def listar_materiales(curso_id):
    retorno    = None
    connection = get_connection()
    cursor     = connection.cursor(dictionary=True)

    query = """
        SELECT id, titulo, url_archivo, fecha_subida
        FROM materiales
        WHERE curso_id = %s
        ORDER BY fecha_subida DESC
    """
    cursor.execute(query, (curso_id,))
    materiales_db = cursor.fetchall()

    cursor.close()
    connection.close()

    materiales = []
    for m in materiales_db:
        fecha_str = m["fecha_subida"].strftime("%Y-%m-%dT%H:%M:%SZ") if hasattr(m["fecha_subida"], "strftime") else str(m["fecha_subida"])
        materiales.append({
            "id":          m["id"],
            "titulo":      m["titulo"],
            "url_archivo": m["url_archivo"],
            "fecha_subida": fecha_str
        })

    retorno = materiales
    return retorno


def guardar_material(titulo, url_archivo, curso_id):
    retorno = None
    try:
        connection = get_connection()
        cursor     = connection.cursor(dictionary=True)

        query = "INSERT INTO materiales (curso_id, titulo, url_archivo) VALUES (%s, %s, %s)"
        cursor.execute(query, (curso_id, titulo, url_archivo))
        connection.commit()

        cursor.close()
        connection.close()

        retorno = {"mensaje": "Material subido exitosamente."}
    except Exception as e:
        retorno = {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}

    return retorno


def eliminar_material(id_material):
    retorno    = None
    connection = get_connection()
    cursor     = connection.cursor(dictionary=True)

    cursor.execute("SELECT url_archivo FROM materiales WHERE id = %s", (id_material,))
    material = cursor.fetchone()

    if not material:
        cursor.close()
        connection.close()
        retorno = {"error": "NOT_FOUND", "mensaje": "Material no encontrado."}
    else:
        url_archivo = material["url_archivo"]
        cursor.execute("DELETE FROM materiales WHERE id = %s", (id_material,))
        connection.commit()
        cursor.close()
        connection.close()

        retorno = {"mensaje": "Material eliminado exitosamente."}

    return retorno
