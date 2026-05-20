from flask import Blueprint, jsonify, request
from validators.alumnos import validar_get_alumnos, validar_id_entero
from services.alumnos import obtener_todos_los_alumnos
from db import execute  # Usamos execute para los GETs simples de sub-recursos

alumnos_bp = Blueprint('alumnos', __name__)


# 1. GET /alumnos (Con paginación y filtros)
@alumnos_bp.route('/alumnos', methods=['GET'])
def get_alumnos():

    # Pasar por el validador 
    error_validacion = validar_get_alumnos()
    if error_validacion:
        return jsonify(error_validacion[0]), error_validacion[1]
    
    # Si pasa la validación, va al servicio 
    resultado, status_code = obtener_todos_los_alumnos()
    return jsonify(resultado), status_code



# 2. GET /alumnos/{id} (Detalle de un alumno)
@alumnos_bp.route('/alumnos/<id_url>', methods=['GET'])
def get_alumno_por_id(id_url):

    # Valida que el ID de la URL sea un entero válido
    id_int, error_val = validar_id_entero(id_url)
    if error_val:
        return jsonify(error_val[0]), error_val[1]
        
    # Consulta a la base de datos si existe el alumno
    query = f"SELECT id, legajo, nombre, apellido, email, abandono FROM alumnos WHERE id = {id_int}"
    alumno = execute(query)
    
    if not alumno:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id_int} no encontrado", "level": "error"}]}), 404
        
    return jsonify(alumno[0]), 200



# 3. GET /alumnos/{id}/notas (Notas del alumno)
@alumnos_bp.route('/alumnos/<id_url>/notas', methods=['GET'])
def get_notas_alumno(id_url):
    id_int, error_val = validar_id_entero(id_url)
    if error_val:
        return jsonify(error_val[0]), error_val[1]
        
    # Se verifica si el alumno existe para tirar 404 si corresponde
    if not execute(f"SELECT id FROM alumnos WHERE id = {id_int}"):
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id_int} no encontrado", "level": "error"}]}), 404
        
    # Se trae las notas cruzando con la tabla de tipos_evaluacion para sacar el nombre (Parcial, TP, etc.)
    query = f"""
        SELECT t.nombre AS evaluacion, n.nota, n.fecha_carga 
        FROM notas n
        JOIN tipos_evaluacion t ON n.id_evaluacion = t.id
        WHERE n.id_alumno = {id_int}
    """
    notas = execute(query)
    return jsonify(notas), 200



# 4. GET /alumnos/{id}/asistencias (Asistencias del alumno)
@alumnos_bp.route('/alumnos/<id_url>/asistencias', methods=['GET'])
def get_asistencias_alumno(id_url):
    id_int, error_val = validar_id_entero(id_url)
    if error_val:
        return jsonify(error_val[0]), error_val[1]
        
    # Verificar si el alumno existe
    if not execute(f"SELECT id FROM alumnos WHERE id = {id_int}"):
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": f"Alumno con ID {id_int} no encontrado", "level": "error"}]}), 404
        
    # Traer historial de asistencias formateando la fecha a string
    query = f"SELECT DATE_FORMAT(fecha, '%Y-%m-%d') as fecha, estado as presente FROM asistencias WHERE id_alumno = {id_int}"
    asistencias = execute(query)
    
    # se mapea el estado de la BD ('presente', 'ausente') a lo que pida el swagger (ej: true/false o el string)
    # En teoria, según la tabla guardo un VARCHAR 'presente', y devuelvo la lista tal cual.
    return jsonify(asistencias), 200
