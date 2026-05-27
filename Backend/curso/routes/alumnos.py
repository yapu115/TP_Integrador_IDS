# Módulos estándar
import csv
import io
import os

# Módulos de terceros (Flask)
from flask import Blueprint, jsonify, request

# Módulos propios del proyecto (agrupados por funcionalidad)
from curso.utils.security import token_required
from curso.validators.alumnos import (
    validar_get_alumnos,
    validar_crear_alumno,
    validar_actualizar_alumno,
    validar_csv_import,
)
from curso.services.alumnos import (
    obtener_todos_los_alumnos,
    obtener_alumno_por_id,
    insertar_alumno,
    importar_desde_csv,
    actualizar_alumno,
    eliminar_alumno,
)
from curso.services.notas import devolver_notas
from flask import render_template

alumnos_bp = Blueprint('alumnos', __name__)

@alumnos_bp.route('/alumnos', methods=['GET'])
#@token_required
def get_alumnos():

    # Pasar por el validador
    error_validacion = validar_get_alumnos()
    if error_validacion:
        return jsonify(error_validacion[0]), error_validacion[1]

    # Si pasa la validación, va al servicio
    resultado, status_code = obtener_todos_los_alumnos()
    
    # --- AQUÍ ESTÁ EL CAMBIO ---
    # Si la petición viene de un navegador (para ver la página), devolvemos el HTML
    return render_template('alumnos.html', alumnos=resultado)

"""
# 1. GET /alumnos (Con paginación y filtros)
@alumnos_bp.route('/alumnos', methods=['GET'])
#@token_required
def get_alumnos():

    # Pasar por el validador
    error_validacion = validar_get_alumnos()
    if error_validacion:
        return jsonify(error_validacion[0]), error_validacion[1]

    # Si pasa la validación, va al servicio
    resultado, status_code = obtener_todos_los_alumnos()
    if status_code == 204:
        return '', 204
    return jsonify(resultado), status_code
"""

# 2. GET /alumnos/{id} (Detalle de un alumno)
@alumnos_bp.route('/alumnos/<int:id>', methods=['GET'])
#@token_required
def get_alumno_por_id(id):
    alumno = obtener_alumno_por_id(id)

    if not alumno:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado", "level": "error"}]}), 404

    return jsonify(alumno), 200


# 3. GET /alumnos/{id}/notas (Notas del alumno)
@alumnos_bp.route('/alumnos/<int:id>/notas', methods=['GET'])
#@token_required
def get_notas_alumno(id):

    if not obtener_alumno_por_id(id):
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado", "level": "error"}]}), 404

    notas = devolver_notas(id)
    return jsonify(notas), 200


# 1. POST /alumnos
@alumnos_bp.route('/alumnos', methods=['POST'])
#@token_required
def crear_alumno():
    data = request.get_json()

    errores, datos_validados = validar_crear_alumno(data)
    if errores:
        return jsonify({"errors": errores}), 400

    resultado = insertar_alumno(datos_validados)
    if resultado:
        return jsonify({
            "errors": [{
                "code": resultado["error"],
                "message": resultado["mensaje"],
                "level": "error"
            }]
        }), 409

    return '', 201


# 2. POST /alumnos/importar
@alumnos_bp.route('/alumnos/importar', methods=['POST'])
#@token_required
def importar_alumnos():
    if 'file' not in request.files:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "No se envió archivo", "level": "error"}]}), 400

    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = list(csv.DictReader(stream))

    errores, filas = validar_csv_import(csv_reader)
    if errores:
        return jsonify({"errors": errores}), 400

    procesados, error = importar_desde_csv(filas)
    if error:
        return jsonify({
            "errors": [{
                "code": error["error"],
                "message": error["mensaje"],
                "level": "error"
            }]
        }), 409

    return jsonify({"procesados": procesados}), 200


# 1. PATCH /alumnos/{id}
@alumnos_bp.route('/alumnos/<int:id>', methods=['PATCH'])
#@token_required
def marcar_abandono(id):
    data = request.get_json()

    errores, datos_validados = validar_actualizar_alumno(data)
    if errores:
        return jsonify({"errors": errores}), 400

    resultado = actualizar_alumno(id, datos_validados)
    if resultado:
        return jsonify({
            "errors": [{
                "code": resultado["error"],
                "message": resultado["mensaje"],
                "level": "error"
            }]
        }), 404

    return '', 204


# 1. DELETE /alumnos/{id}
@alumnos_bp.route('/alumnos/<int:id>', methods=['DELETE'])
#@token_required
def borrar_alumno(id):
    resultado = eliminar_alumno(id)
    if resultado:
        return jsonify({
            "errors": [{
                "code": resultado["error"],
                "message": resultado["mensaje"],
                "level": "error"
            }]
        }), 404

    return '', 204
