# Módulos estándar
import csv
import io

# Módulos de terceros (Flask)
from flask import Blueprint, jsonify, request
import datetime

# Módulos propios del proyecto
from curso.utils.security import token_required, role_required
from curso.services.cursos import curso_existe
from curso.validators.alumnos import validar_get_alumnos
from curso.services.alumnos import (
    obtener_todos_los_alumnos,
    insertar_alumno,
    importar_desde_csv,
    eliminar_alumno,
    obtener_portal_alumno_por_padron,
)
from curso.db import get_connection

alumnos_bp = Blueprint('alumnos', __name__)


@alumnos_bp.route('/alumnos/portal', methods=['GET'])
def portal_alumno():
    padron = (request.args.get("padron") or "").strip()
    if not padron:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Debe ingresar un numero de padron."}]}), 400

    resultado = obtener_portal_alumno_por_padron(padron)
    if "error" in resultado:
        status_code = 404 if resultado["error"] == "NOT_FOUND" else 500
        return jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), status_code

    for curso in resultado.get('cursos', []):
        for nota in curso.get('notas', []):
            if 'hora' in nota and isinstance(nota['hora'], datetime.timedelta):
                # Convierte '1 day, 2:00:00' a un formato string que JSON acepta
                nota['hora'] = str(nota['hora']) 

    return jsonify(resultado), 200



def get_curso_id():
    """Devuelve (curso_id, None) si es válido, o (None, respuesta_error) si no."""
    raw = request.args.get("curso_id")
    if not raw:
        return None, (jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Se requiere el parámetro 'curso_id'."}]}), 400)
    try:
        cid = int(raw)
    except ValueError:
        return None, (jsonify({"errors": [{"code": "BAD_REQUEST", "message": "El parámetro 'curso_id' debe ser un entero."}]}), 400)
    if not curso_existe(cid):
        return None, (jsonify({"errors": [{"code": "NOT_FOUND", "message": f"No existe un curso con id={cid}."}]}), 404)
    return cid, None


@alumnos_bp.route('/alumnos', methods=['GET'])
@token_required
def get_alumnos():
    curso_id, error = get_curso_id()
    if error:
        return error

    error_validacion = validar_get_alumnos()
    if error_validacion:
        return jsonify(error_validacion[0]), error_validacion[1]

    resultado, status_code = obtener_todos_los_alumnos(curso_id)
    if status_code == 204:
        return "", 204
    return jsonify(resultado), status_code


@alumnos_bp.route('/alumnos/<int:id>', methods=['GET'])
@token_required
def get_alumno_por_id(id):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, legajo, nombre, apellido, email, abandono, curso_id FROM alumnos WHERE id = %s", (id,))
    alumno = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not alumno:
        retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado"}]}), 404
    else:
        retorno = jsonify(alumno), 200
    return retorno



@alumnos_bp.route('/alumnos/<int:id>/notas', methods=['GET'])
@token_required
def get_notas_alumno(id):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id FROM alumnos WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conexion.close()
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado"}]}), 404

    query = """
        SELECT t.nombre AS evaluacion, n.nota, n.fecha_carga
        FROM notas n
        JOIN tipos_evaluacion t ON n.id_evaluacion = t.id
        WHERE n.id_alumno = %s
    """
    cursor.execute(query, (id,))
    notas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(notas), 200



@alumnos_bp.route('/alumnos/<int:id>/asistencias', methods=['GET'])
@token_required
def get_asistencias_alumno(id):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id FROM alumnos WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conexion.close()
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado"}]}), 404

    cursor.execute(
        "SELECT DATE_FORMAT(fecha, '%Y-%m-%d') as fecha, estado as presente FROM asistencias WHERE id_alumno = %s",
        (id,)
    )
    asistencias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(asistencias), 200


@alumnos_bp.route('/alumnos', methods=['POST'])
@token_required
def crear_alumno():
    curso_id, error = get_curso_id()
    if error:
        return error

    data = request.get_json(silent=True) or {}
    campos_requeridos = ['legajo', 'nombre', 'apellido', 'email']
    faltantes = [c for c in campos_requeridos if not data.get(c)]
    if faltantes:
        return jsonify({"errors": [{"code": "VALIDATION_ERROR", "message": f"Faltan campos obligatorios: {', '.join(faltantes)}"}]}), 400

    insertar_alumno(data, curso_id)
    return jsonify({"message": "Alumno creado exitosamente"}), 201


@alumnos_bp.route('/alumnos/importar', methods=['POST'])
@token_required
def importar_alumnos():
    curso_id, error = get_curso_id()
    if error:
        return error

    if 'file' not in request.files:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "No se envió archivo"}]}), 400

    file       = request.files['file']
    stream     = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = list(csv.DictReader(stream))

    importar_desde_csv(csv_reader, curso_id)
    return jsonify({"procesados": len(csv_reader)}), 200



@alumnos_bp.route('/alumnos/<int:id>', methods=['PATCH'])
@token_required
def actualizar_alumno(id):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id FROM alumnos WHERE id = %s", (id,))
    existe = cursor.fetchone()

    if not existe:
        cursor.close()
        conexion.close()
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado"}]}), 404

    data = request.get_json(silent=True) or {}
    campos_permitidos = {
        "nombre": "nombre",
        "apellido": "apellido",
        "email": "email",
        "abandono": "abandono",
    }
    campos_update = []
    valores = []

    for campo_json, campo_sql in campos_permitidos.items():
        if campo_json in data:
            campos_update.append(f"{campo_sql} = %s")
            valores.append(data[campo_json])

    if not campos_update:
        cursor.close()
        conexion.close()
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Debe enviar al menos un campo editable."}]}), 400

    valores.append(id)
    query = f"UPDATE alumnos SET {', '.join(campos_update)} WHERE id = %s"
    cursor.execute(query, tuple(valores))
    conexion.commit()

    cursor.close()
    conexion.close()
    return jsonify({"message": "Alumno actualizado"}), 200


@alumnos_bp.route('/alumnos/<int:id>', methods=['DELETE'])
@token_required
@role_required
def borrar_alumno(id):
    conexion = get_connection()
    cursor   = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id FROM alumnos WHERE id = %s", (id,))
    existe = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not existe:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado"}]}), 404

    eliminar_alumno(id)
    return "", 204
