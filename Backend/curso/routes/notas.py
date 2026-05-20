from flask import Blueprint, request, jsonify
from curso.validators.notas import validar_notas
from curso.services.notas import evaluacion_existe, alumno_existe, crear_nota, devolver_notas

notas_bp = Blueprint("notas", __name__)

@notas_bp.route("/notas", methods=["PUT"])
def notas():
    data = request.get_json()

    if not data:
        return jsonify({
            "errors": [
                {
                    "code": "VALIDATION_ERROR",
                    "message": "El formato de los datos enviados es inválido.",
                    "level": "error",
                    "description": "El body de la request es requerido."
                }
            ]
        }), 400

    errores = validar_notas(data)

    if errores:
        return jsonify({
            "errors": errores
        }), 400

    if not alumno_existe(data):
        return jsonify({
            "errors": [
                {
                    "code": "NOT_FOUND",
                    "message": "Recurso no encontrado",
                    "level": "error",
                    "description": "El alumno con esa id no existe."
                }
            ]
        }), 404

    if not evaluacion_existe(data):
        return jsonify({
            "errors": [
                {
                    "code": "NOT_FOUND",
                    "message": "Recurso no encontrado",
                    "level": "error",
                    "description": "La evaluacion con esa id no existe."
                }
            ]
        }), 404

    crear_nota(data)

    return "", 204
    

@notas_bp.route("/alumnos/<int:id_alumno>/notas", methods=["GET"])
def obtener_notas_alumno(id_alumno):
    try:
        notas = devolver_notas(id_alumno)

        if len(notas) == 0:
            return jsonify({
                "errors": [
                    {
                        "code": "NOT_FOUND",
                        "message": "Recurso no encontrado",
                        "level": "error",
                        "description": "El recurso solicitado no existe en la base de datos."
                    }
                ]
            }), 404

        return jsonify(notas), 200

    except Exception as e:
        return jsonify({
            "errors": [
                {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Error interno del servidor",
                    "level": "error",
                    "description": "Ocurrió un error inesperado. Por favor, intente más tarde."
                }
            ]
        }), 500


