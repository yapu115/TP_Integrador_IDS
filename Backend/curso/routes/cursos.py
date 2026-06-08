from flask import Blueprint, jsonify, request
from curso.utils.security import token_required, role_required
from curso.validators.cursos import validar_curso
from curso.services.cursos import (
    listar_cursos,
    obtener_curso,
    crear_curso,
    modificar_curso,
    eliminar_curso,
)

cursos_bp = Blueprint("cursos", __name__)


@cursos_bp.route("/cursos", methods=["GET"])
@token_required
def route_listar_cursos():
    resultado = listar_cursos()
    if resultado is None:
        retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error al listar cursos."}]}), 500
    else:
        retorno = jsonify(resultado), 200
    return retorno


@cursos_bp.route("/cursos/<int:curso_id>", methods=["GET"])
@token_required
@role_required("admin")
def route_obtener_curso(curso_id):
    resultado = obtener_curso(curso_id)
    if "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
        else:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
    else:
        retorno = jsonify(resultado), 200
    return retorno


@cursos_bp.route("/cursos", methods=["POST"])
@token_required
@role_required("admin")
def route_crear_curso():
    data = request.get_json(silent=True) or {}
    errores = validar_curso(data)
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = crear_curso(data)
        if "error" in resultado:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = jsonify(resultado), 201
    return retorno



@cursos_bp.route("/cursos/<int:curso_id>", methods=["PUT"])
@token_required
@role_required("admin")
def route_modificar_curso(curso_id):
    data = request.get_json(silent=True) or {}
    errores = validar_curso(data)
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = modificar_curso(curso_id, data)
        if "error" in resultado:
            if resultado["error"] == "NOT_FOUND":
                retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
            else:
                retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = "", 204
    return retorno


@cursos_bp.route("/cursos/<int:curso_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def route_eliminar_curso(curso_id):
    resultado = eliminar_curso(curso_id)
    if "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
        else:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
    else:
        retorno = "", 204
    return retorno
