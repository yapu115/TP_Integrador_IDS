import mysql.connector
from flask import request

from curso.db import execute, get_connection


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

    prev_offset = max(0, offset - limit) if offset > 0 else 0
    links["_prev"] = {"href": f"{base_url}?_offset={prev_offset}&_limit={limit}{filtro_abandono}"}

    if offset + limit < total_registros:
        next_offset = offset + limit
        links["_next"] = {"href": f"{base_url}?_offset={next_offset}&_limit={limit}{filtro_abandono}"}
    else:
        links["_next"] = {"href": f"{base_url}?_offset={offset}&_limit={limit}{filtro_abandono}"}

    last_offset = ((total_registros - 1) // limit) * limit if total_registros > 0 else 0
    links["_last"] = {"href": f"{base_url}?_offset={last_offset}&_limit={limit}{filtro_abandono}"}

    return links


def _normalizar_alumno(alumno):
    if not alumno:
        return None
    resultado = dict(alumno)
    if 'abandono' in resultado:
        resultado['abandono'] = bool(resultado['abandono'])
    if 'legajo' in resultado:
        resultado['legajo'] = str(resultado['legajo'])
    return resultado

# Esto lo pones dentro de curso/services/alumnos.py
def obtener_todos_los_alumnos():
    # Retornamos datos falsos para ver el diseño en el navegador
    datos_fake = [
        {"legajo": "1001", "nombre": "Juan", "apellido": "Perez", "email": "juan@perez.com"},
        {"legajo": "1002", "nombre": "Maria", "apellido": "Garcia", "email": "maria@garcia.com"}
    ]
    # Retornamos los datos y un código 200 (OK)
    return datos_fake, 200

"""
# PRE: Cliente realizó un GET a /alumnos. Módulo 'db.execute' disponible.
# POST: Retorna (respuesta_dict, 200) o (None, 204) si la base de datos está vacía.
def obtener_todos_los_alumnos():
    limit, offset, abandono_raw = _extraer_parametros()
    where_str = _construir_filtro_sql(abandono_raw)

    query_count = f"SELECT COUNT(*) as total FROM alumnos {where_str}"
    count_result = execute(query_count)
    total_registros = count_result[0]['total'] if count_result else 0

    if total_registros == 0:
        return None, 204

    query_alumnos = f"SELECT id, legajo, nombre, apellido FROM alumnos {where_str} LIMIT {limit} OFFSET {offset}"
    alumnos = execute(query_alumnos)

    for alumno in alumnos:
        if 'legajo' in alumno:
            alumno['legajo'] = str(alumno['legajo'])

    links = _generar_links_hateoas(request.base_url, limit, offset, total_registros, abandono_raw)

    respuesta = {
        "alumnos": alumnos,
        "_links": links
    }

    return respuesta, 200
"""

def obtener_alumno_por_id(id_alumno):
    query = "SELECT id, legajo, nombre, apellido, email, abandono FROM alumnos WHERE id = %s"
    resultado = execute(query, (id_alumno,))
    if not resultado:
        return None
    return _normalizar_alumno(resultado[0])


#-- 2.Funciones para Post --

#2.1.Funcion para POST /alumnos

# Pre: data contiene 'legajo', 'nombre', 'apellido', 'email'
# Post: alumno insertado en tabla 'alumnos' o dict con error
def insertar_alumno(data):
    query = "INSERT INTO alumnos (legajo, nombre, apellido, email) VALUES (%s, %s, %s, %s)"
    try:
        execute(query, (data['legajo'], data['nombre'], data['apellido'], data['email']))
        return None
    except mysql.connector.IntegrityError:
        return {
            "error": "RESOURCE_ALREADY_EXISTS",
            "mensaje": "Ya existe un alumno con ese legajo."
        }


#2.2.Funcion para POST /alumnos/importar

# Pre: rows es lista de dicts con 'legajo', 'nombre', 'apellido', 'email'
# Post: todos los alumnos insertados en tabla 'alumnos'
def importar_desde_csv(rows):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO alumnos (legajo, nombre, apellido, email) VALUES (%s, %s, %s, %s)"
    try:
        for row in rows:
            cursor.execute(query, (row['legajo'], row['nombre'], row['apellido'], row['email']))
        connection.commit()
        return len(rows), None
    except mysql.connector.IntegrityError:
        connection.rollback()
        return None, {
            "error": "RESOURCE_ALREADY_EXISTS",
            "mensaje": "El CSV contiene un legajo duplicado o ya registrado."
        }
    finally:
        cursor.close()
        connection.close()


#-- 3.funcion para Patch --

# Pre: datos contiene al menos un campo permitido (nombre, apellido, email, abandono)
# Post: se actualiza el alumno o se retorna error
def actualizar_alumno(id_alumno, datos):
    if not execute("SELECT id FROM alumnos WHERE id = %s", (id_alumno,)):
        return {"error": "NOT_FOUND", "mensaje": f"Alumno con ID {id_alumno} no encontrado"}

    sets = []
    valores = []
    for campo, valor in datos.items():
        sets.append(f"{campo} = %s")
        valores.append(valor)

    query = f"UPDATE alumnos SET {', '.join(sets)} WHERE id = %s"
    valores.append(id_alumno)
    execute(query, tuple(valores))
    return None


#-- 4.Funcion para Delete --

# Pre: id_alumno es un entero válido
# Post: se elimina el registro del alumno de la tabla alumnos
def eliminar_alumno(id_alumno):
    filas = execute("DELETE FROM alumnos WHERE id = %s", (id_alumno,))
    if filas == 0:
        return {"error": "NOT_FOUND", "mensaje": f"Alumno con ID {id_alumno} no encontrado"}
    return None
