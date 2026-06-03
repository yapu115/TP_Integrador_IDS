from flask import request
from curso.db import get_connection




def _extraer_parametros():
    limit       = request.args.get('_limit',   default=10,   type=int)
    offset      = request.args.get('_offset',  default=0,    type=int)
    abandono_raw = request.args.get('abandono', default=None)
    if limit  < 1: limit  = 10
    if offset < 0: offset = 0
    return limit, offset, abandono_raw


def _construir_filtro_abandono(abandono_raw):
    if abandono_raw is None:
        return ""
    if abandono_raw.lower() == 'true':
        return "AND abandono = 1"
    if abandono_raw.lower() == 'false':
        return "AND abandono = 0"
    return ""


def _generar_links_hateoas(base_url, limit, offset, total, abandono_raw, curso_id):
    filtro = f"&abandono={abandono_raw}" if abandono_raw is not None else ""
    base  = f"{base_url}?curso_id={curso_id}"

    prev_offset = max(0, offset - limit)
    next_offset = offset + limit
    last_offset = ((total - 1) // limit) * limit if total > 0 else 0

    return {
        "_first": {"href": f"{base}&_offset=0&_limit={limit}{filtro}"},
        "_prev":  {"href": f"{base}&_offset={prev_offset}&_limit={limit}{filtro}"},
        "_next":  {"href": f"{base}&_offset={next_offset}&_limit={limit}{filtro}"} if next_offset < total else None,
        "_last":  {"href": f"{base}&_offset={last_offset}&_limit={limit}{filtro}"},
    }


def obtener_todos_los_alumnos(curso_id):
    limit, offset, abandono_raw = _extraer_parametros()
    filtro_abandono = _construir_filtro_abandono(abandono_raw)

    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)

    query_count = f"SELECT COUNT(*) as total FROM alumnos WHERE curso_id = %s {filtro_abandono}"
    cursor.execute(query_count, (curso_id,))
    total = cursor.fetchone()["total"]

    if total == 0:
        cursor.close()
        conexion.close()
        return "", 204

    query_alumnos = f"""
        SELECT id, legajo, nombre, apellido, email, abandono
        FROM alumnos
        WHERE curso_id = %s {filtro_abandono}
        ORDER BY id
        LIMIT %s OFFSET %s
    """
    cursor.execute(query_alumnos, (curso_id, limit, offset))
    alumnos = cursor.fetchall()

    cursor.close()
    conexion.close()

    links = _generar_links_hateoas(request.base_url, limit, offset, total, abandono_raw, curso_id)
    return {"alumnos": alumnos, "_links": links}, 200


def insertar_alumno(data, curso_id):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)
    query    = "INSERT INTO alumnos (curso_id, legajo, nombre, apellido, email) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (curso_id, data['legajo'], data['nombre'], data['apellido'], data['email']))
    conexion.commit()
    cursor.close()
    conexion.close()


def importar_desde_csv(rows, curso_id):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)
    query    = "INSERT INTO alumnos (curso_id, legajo, nombre, apellido, email) VALUES (%s, %s, %s, %s, %s)"
    for row in rows:
        cursor.execute(query, (curso_id, row['legajo'], row['nombre'], row['apellido'], row['email']))
    conexion.commit()
    cursor.close()
    conexion.close()



def actualizar_abandono(id_alumno, estado):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)
    cursor.execute("UPDATE alumnos SET abandono = %s WHERE id = %s", (estado, id_alumno))
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_alumno(id_alumno):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)
    cursor.execute("DELETE FROM alumnos WHERE id = %s", (id_alumno,))
    conexion.commit()
    cursor.close()
    conexion.close()


def alumno_en_curso(id_alumno, curso_id):
    conexion = get_connection()
    cursor   = conexion.cursor()
    cursor.execute("SELECT 1 FROM alumnos WHERE id = %s AND curso_id = %s", (id_alumno, curso_id))
    existe = cursor.fetchone() is not None
    cursor.close()
    conexion.close()
    return existe
