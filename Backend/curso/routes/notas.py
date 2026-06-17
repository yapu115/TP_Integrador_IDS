from flask import Blueprint, request, jsonify
from curso.validators.notas import validar_notas
from curso.services.notas import evaluacion_existe, alumno_existe, crear_nota
from curso.utils.security import token_required

notas_bp = Blueprint("notas", __name__)

@notas_bp.route("/notas", methods=["PUT"])
@token_required
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
    




