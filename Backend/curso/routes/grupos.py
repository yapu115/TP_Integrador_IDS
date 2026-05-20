from flask import Blueprint, jsonify, request
from curso.utils.security import token_required
from curso.validators.grupos import validar_grupo
from curso.services.grupos import (
    listar_grupos,
    obtener_grupo,
    crear_grupo,
    modificar_grupo,
    eliminar_grupo
)

grupos_bp = Blueprint("grupos", __name__)

@grupos_bp.route("/grupos", methods=["GET"])
@token_required
def route_listar_grupos():
    retorno = None
    resultado = listar_grupos()
    
    if resultado is None:
        retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error al listar grupos."}]}), 500
    else:
        retorno = jsonify(resultado), 200
        
    return retorno

@grupos_bp.route("/grupos", methods=["POST"])
@token_required
def route_crear_grupo():
    retorno = None
    data = request.get_json(silent=True) or {}
    
    errores = validar_grupo(data)
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = crear_grupo(data)
        if "error" in resultado:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = "", 201
            
    return retorno

@grupos_bp.route("/grupos/<int:id_grupo>", methods=["GET"])
@token_required
def route_obtener_grupo(id_grupo):
    retorno = None
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
def route_modificar_grupo(id_grupo):
    retorno = None
    data = request.get_json(silent=True) or {}
    
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
def route_eliminar_grupo(id_grupo):
    retorno = None
    resultado = eliminar_grupo(id_grupo)
    
    if "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
        else:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
    else:
        retorno = "", 204
        
    return retorno