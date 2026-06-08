from flask import request
from curso.db import get_connection
from decimal import Decimal




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


def _serializar_valor(valor):
    if hasattr(valor, "isoformat"):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return float(valor)
    return valor


def _serializar_fila(fila):
    return {clave: _serializar_valor(valor) for clave, valor in fila.items()}


def _obtener_notas_alumno(cursor, alumno_id):
    cursor.execute(
        """
        SELECT te.id, te.nombre, te.descripcion, te.fecha, te.hora,
               n.nota, n.fecha_carga
        FROM notas n
        INNER JOIN tipos_evaluacion te ON te.id = n.id_evaluacion
        WHERE n.id_alumno = %s
        ORDER BY te.fecha IS NULL, te.fecha, te.id
        """,
        (alumno_id,),
    )
    return [_serializar_fila(fila) for fila in cursor.fetchall()]


def _obtener_materiales_curso(cursor, curso_id):
    cursor.execute(
        """
        SELECT id, titulo, url_archivo, fecha_subida
        FROM materiales
        WHERE curso_id = %s
        ORDER BY fecha_subida DESC
        """,
        (curso_id,),
    )
    return [_serializar_fila(fila) for fila in cursor.fetchall()]


def _obtener_asistencias_alumno(cursor, alumno_id):
    cursor.execute(
        """
        SELECT id_asistencia, fecha, estado, creado_en
        FROM asistencias
        WHERE id_alumno = %s
        ORDER BY fecha DESC
        """,
        (alumno_id,),
    )
    return [_serializar_fila(fila) for fila in cursor.fetchall()]


def _obtener_grupos_alumno(cursor, alumno_id, curso_id):
    cursor.execute(
        """
        SELECT g.id, g.nombre_grupo
        FROM grupos g
        INNER JOIN grupo_integrantes gi ON gi.id_grupo = g.id
        WHERE gi.id_alumno = %s AND g.curso_id = %s
        ORDER BY g.nombre_grupo
        """,
        (alumno_id, curso_id),
    )
    grupos = []
    for grupo in cursor.fetchall():
        cursor.execute(
            """
            SELECT a.id, a.legajo, a.nombre, a.apellido, a.email
            FROM grupo_integrantes gi
            INNER JOIN alumnos a ON a.id = gi.id_alumno
            WHERE gi.id_grupo = %s
            ORDER BY a.apellido, a.nombre
            """,
            (grupo["id"],),
        )
        integrantes = [_serializar_fila(fila) for fila in cursor.fetchall()]

        cursor.execute(
            """
            SELECT te.id, te.nombre, te.descripcion
            FROM grupo_evaluaciones ge
            INNER JOIN tipos_evaluacion te ON te.id = ge.id_evaluacion
            WHERE ge.id_grupo = %s
            ORDER BY te.id
            """,
            (grupo["id"],),
        )
        evaluaciones = [_serializar_fila(fila) for fila in cursor.fetchall()]

        grupos.append({
            "id": grupo["id"],
            "nombre": grupo["nombre_grupo"],
            "integrantes": integrantes,
            "evaluaciones": evaluaciones,
        })
    return grupos


def obtener_portal_alumno_por_padron(padron):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                a.id AS alumno_id,
                a.legajo,
                a.nombre AS alumno_nombre,
                a.apellido,
                a.email,
                a.abandono,
                c.id AS curso_id,
                c.nombre AS curso_nombre,
                c.descripcion,
                c.fecha_inicio,
                c.fecha_fin,
                c.activo
            FROM alumnos a
            INNER JOIN cursos c ON c.id = a.curso_id
            WHERE a.legajo = %s
            ORDER BY c.nombre
            """,
            (padron,),
        )
        filas = cursor.fetchall()

        if not filas:
            return {"error": "NOT_FOUND", "mensaje": "No se encontro ningun alumno con ese padron."}

        cursos = []
        for fila in filas:
            alumno_id = fila["alumno_id"]
            curso_id = fila["curso_id"]
            cursos.append({
                "alumno": {
                    "id": alumno_id,
                    "padron": fila["legajo"],
                    "nombre": fila["alumno_nombre"],
                    "apellido": fila["apellido"],
                    "email": fila["email"],
                    "abandono": bool(fila["abandono"]),
                },
                "curso": {
                    "id": curso_id,
                    "nombre": fila["curso_nombre"],
                    "descripcion": fila["descripcion"],
                    "fecha_inicio": _serializar_valor(fila["fecha_inicio"]),
                    "fecha_fin": _serializar_valor(fila["fecha_fin"]),
                    "activo": bool(fila["activo"]),
                },
                "notas": _obtener_notas_alumno(cursor, alumno_id),
                "materiales": _obtener_materiales_curso(cursor, curso_id),
                "grupos": _obtener_grupos_alumno(cursor, alumno_id, curso_id),
                "asistencias": _obtener_asistencias_alumno(cursor, alumno_id),
            })

        alumno_base = cursos[0]["alumno"]
        return {
            "padron": padron,
            "alumno": alumno_base,
            "cursos": cursos,
        }
    except Exception as e:
        return {"error": "INTERNAL_SERVER_ERROR", "mensaje": str(e)}
    finally:
        cursor.close()
        conexion.close()
