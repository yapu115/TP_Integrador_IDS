from flask import Blueprint, jsonify, request
from curso.utils.security import token_required
from curso.utils.utils import registrar_actividad
from curso.validators.grupos import validar_grupo
from curso.services.cursos import curso_existe
from curso.services.grupos import (
    listar_grupos,
    obtener_grupo,
    crear_grupo,
    modificar_grupo,
    eliminar_grupo,
)

grupos_bp = Blueprint("grupos", __name__)


def get_curso_id():
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



@grupos_bp.route("/grupos", methods=["GET"])
@token_required
def route_listar_grupos():
    curso_id, error = get_curso_id()
    if error:
        return error

    resultado = listar_grupos(curso_id)
    if resultado is None:
        retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error al listar grupos."}]}), 500
    else:
        retorno = jsonify(resultado), 200
    return retorno


@grupos_bp.route("/grupos", methods=["POST"])
@token_required
@registrar_actividad("CREACION_GRUPO")
def route_crear_grupo():
    curso_id, error = get_curso_id()
    if error:
        return error

    data    = request.get_json(silent=True) or {}
    errores = validar_grupo(data)
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = crear_grupo(data, curso_id)
        if "error" in resultado:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = jsonify(resultado), 201
    return retorno


@grupos_bp.route("/grupos/<int:id_grupo>", methods=["GET"])
@token_required
def route_obtener_grupo(id_grupo):
    resultado = obtener_grupo(id_grupo)
    if resultado is None:
        retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error inesperado."}]}), 500
    elif "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
        else:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
    else:
        retorno = jsonify(resultado), 200
    return retorno


@grupos_bp.route("/grupos/<int:id_grupo>", methods=["PUT"])
@token_required
@registrar_actividad("MODIFICACION_GRUPO")
def route_modificar_grupo(id_grupo):
    data    = request.get_json(silent=True) or {}
    errores = validar_grupo(data)
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = modificar_grupo(id_grupo, data)
        if "error" in resultado:
            if resultado["error"] == "NOT_FOUND":
                retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
            else:
                retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = "", 204
    return retorno



@grupos_bp.route("/grupos/<int:id_grupo>", methods=["DELETE"])
@token_required
@registrar_actividad("ELIMINAR_GRUPO")
def route_eliminar_grupo(id_grupo):
    resultado = eliminar_grupo(id_grupo)
    if "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
        else:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
    else:
        retorno = "", 204
    return retorno