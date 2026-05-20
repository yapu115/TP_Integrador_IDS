# Módulos estándar
import csv
import io

# Módulos de terceros (Flask)
from flask import Blueprint, jsonify, request

# Módulos propios del proyecto (agrupados por funcionalidad)
from db import execute
from utils.security import token_required
from validators.alumnos import validar_get_alumnos, validar_id_entero
from services.alumnos import (
    obtener_todos_los_alumnos, 
    insertar_alumno, 
    importar_desde_csv,
    actualizar_abandono, 
    eliminar_alumno      
)

alumnos_bp = Blueprint('alumnos', __name__)


# 1. GET /alumnos (Con paginación y filtros)
@alumnos_bp.route('/alumnos', methods=['GET'])
@token_required
def get_alumnos():

    # Pasar por el validador 
    error_validacion = validar_get_alumnos()
    if error_validacion:
        return jsonify(error_validacion[0]), error_validacion[1]
    
    # Si pasa la validación, va al servicio 
    resultado, status_code = obtener_todos_los_alumnos()
    return jsonify(resultado), status_code



# 2. GET /alumnos/{id} (Detalle de un alumno)
@alumnos_bp.route('/alumnos/<int:id>', methods=['GET'])
@token_required
def get_alumno_por_id(id):
    query = "SELECT id, legajo, nombre, apellido, email, abandono FROM alumnos WHERE id = %s"
    alumno = execute(query, (id,))
    
    if not alumno:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado", "level": "error"}]}), 404
        
    return jsonify(alumno[0]), 200



# 3. GET /alumnos/{id}/notas (Notas del alumno)
@alumnos_bp.route('/alumnos/<int:id>/notas', methods=['GET'])
@token_required
def get_notas_alumno(id):

    # Verificación de existencia
    if not execute("SELECT id FROM alumnos WHERE id = %s", (id,)):
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado", "level": "error"}]}), 404
        
    query = """
        SELECT t.nombre AS evaluacion, n.nota, n.fecha_carga 
        FROM notas n
        JOIN tipos_evaluacion t ON n.id_evaluacion = t.id
        WHERE n.id_alumno = %s
    """
    notas = execute(query, (id,))
    return jsonify(notas), 200



# 4. GET /alumnos/{id}/asistencias (Asistencias del alumno)
@alumnos_bp.route('/alumnos/<int:id>/asistencias', methods=['GET'])
@token_required
def get_asistencias_alumno(id):

    if not execute("SELECT id FROM alumnos WHERE id = %s", (id,)):
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id} no encontrado", "level": "error"}]}), 404
        
    query = "SELECT DATE_FORMAT(fecha, '%Y-%m-%d') as fecha, estado as presente FROM asistencias WHERE id_alumno = %s"
    asistencias = execute(query, (id,))
    
    return jsonify(asistencias), 200


# 1. POST /alumnos 
@alumnos_bp.route('/alumnos', methods=['POST'])
@token_required
def crear_alumno():
    data = request.get_json()
    insertar_alumno(data)
    return jsonify({"message": "Alumno creado exitosamente"}), 201

# 2. POST /alumnos/importar 
@alumnos_bp.route('/alumnos/importar', methods=['POST'])
@token_required
def importar_alumnos():
    if 'file' not in request.files:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "No se envió archivo"}]}), 400
    
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = list(csv.DictReader(stream))
    
    importar_desde_csv(csv_reader)
    return jsonify({"procesados": len(csv_reader)}), 200


# 1. PATCH /alumnos/{id} 
@alumnos_bp.route('/alumnos/<int:id>', methods=['PATCH'])
@token_required
def marcar_abandono(id):
    data = request.get_json()
    if not data or 'abandono' not in data:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Falta el campo 'abandono'"}]}), 400
    
    actualizar_abandono(id, data['abandono'])
    return jsonify({"message": "Estado de abandono actualizado"}), 200


# 1. DELETE /alumnos/{id}
@alumnos_bp.route('/alumnos/<int:id>', methods=['DELETE'])
@token_required
def borrar_alumno(id):
    eliminar_alumno(id)
    return jsonify({"message": "Alumno eliminado exitosamente"}), 200