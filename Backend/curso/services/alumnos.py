from flask import request
from db import execute


#-- 1.Funciones para GET --

#1.1.Funciones para GET /alumnos

# PRE: Se debe invocar dentro de una petición HTTP activa de Flask.
# POST: Retorna (limit, offset, abandono_raw). limit >= 1, offset >= 0.
def _extraer_parametros():
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)
    abandono_raw = request.args.get('abandono', default=None)
    
    if limit < 1: limit = 10
    if offset < 0: offset = 0
    
    return limit, offset, abandono_raw

# PRE: 'abandono_raw' debe ser un string ('true'/'false') o None.
# POST: Retorna la cláusula SQL "WHERE..." o un string vacío si no aplica.
def _construir_filtro_sql(abandono_raw):
    where_clauses = []
    if abandono_raw is not None:
        if abandono_raw.lower() == 'true':
            where_clauses.append("abandono = 1")
        elif abandono_raw.lower() == 'false':
            where_clauses.append("abandono = 0")
            
    return f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

# PRE: limit > 0, offset >= 0, total_registros >= 0.
# POST: Retorna el diccionario de links HATEOAS (_first, _prev, _next, _last).
def _generar_links_hateoas(base_url, limit, offset, total_registros, abandono_raw):
    filtro_abandono = f"&abandono={abandono_raw}" if abandono_raw is not None else ""
    
    links = {
        "_first": {"href": f"{base_url}?_offset=0&_limit={limit}{filtro_abandono}"}
    }

    # Anterior
    prev_offset = max(0, offset - limit) if offset > 0 else 0
    links["_prev"] = {"href": f"{base_url}?_offset={prev_offset}&_limit={limit}{filtro_abandono}"}

    # Siguiente
    if offset + limit < total_registros:
        next_offset = offset + limit
        links["_next"] = {"href": f"{base_url}?_offset={next_offset}&_limit={limit}{filtro_abandono}"}
    else:
        links["_next"] = {"href": f"{base_url}?_offset={offset}&_limit={limit}{filtro_abandono}"}

    # Último
    last_offset = ((total_registros - 1) // limit) * limit if total_registros > 0 else 0
    links["_last"] = {"href": f"{base_url}?_offset={last_offset}&_limit={limit}{filtro_abandono}"}

    return links

# PRE: Cliente realizó un GET a /alumnos. Módulo 'db.execute' disponible.
# POST: Retorna (respuesta_dict, 200) o ("", 204) si la base de datos está vacía.
def obtener_todos_los_alumnos():
    limit, offset, abandono_raw = _extraer_parametros()
    where_str = _construir_filtro_sql(abandono_raw)

    query_count = f"SELECT COUNT(*) as total FROM alumnos {where_str}"
    count_result = execute(query_count)
    total_registros = count_result[0]['total'] if count_result else 0

    if total_registros == 0:
        return "", 204

    query_alumnos = f"SELECT id, legajo, nombre, apellido FROM alumnos {where_str} LIMIT {limit} OFFSET {offset}"
    alumnos = execute(query_alumnos)

    links = _generar_links_hateoas(request.base_url, limit, offset, total_registros, abandono_raw)

    respuesta = {
        "alumnos": alumnos,
        "_links": links
    }

    return respuesta, 200

#-- 2.Funciones para Post --

#2.1.Funcion para POST /alumnos

# Pre: data contiene 'legajo', 'nombre', 'apellido', 'email'
# Post: alumno insertado en tabla 'alumnos'
def insertar_alumno(data):
    query = "INSERT INTO alumnos (legajo, nombre, apellido, email) VALUES (%s, %s, %s, %s)"
    execute(query, (data['legajo'], data['nombre'], data['apellido'], data['email']))

#2.2.Funcion para POST /alumnos/importar

# Pre: rows es lista de dicts con 'legajo', 'nombre', 'apellido', 'email'
# Post: todos los alumnos insertados en tabla 'alumnos'
def importar_desde_csv(rows):
    # Como vi que no usamos pandas en reqirements.txt use el módulo csv nativo
    query = "INSERT INTO alumnos (legajo, nombre, apellido, email) VALUES (%s, %s, %s, %s)"
    for row in rows:
        execute(query, (row['legajo'], row['nombre'], row['apellido'], row['email']))

#-- 3.funcion para Patch --

# Pre: estado es un booleano (True/False)
# Post: se actualiza la columna 'abandono' en la tabla alumnos para el id_alumno dado
def actualizar_abandono(id_alumno, estado):
    query = "UPDATE alumnos SET abandono = %s WHERE id = %s"
    execute(query, (estado, id_alumno))

#-- 4.Funcion para Delete --

# Pre: id_alumno es un entero válido
# Post: se elimina el registro del alumno de la tabla alumnos
def eliminar_alumno(id_alumno):
    query = "DELETE FROM alumnos WHERE id = %s"
    execute(query, (id_alumno,))
