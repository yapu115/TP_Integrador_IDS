from flask import Blueprint, request, jsonify
from curso.utils.security import token_required
from curso.validators.materiales import validar_subida_material
from curso.services.materiales import listar_materiales, guardar_material, eliminar_material

materiales_bp = Blueprint("materiales", __name__)

@materiales_bp.route("/materiales", methods=["GET"])
def get_materiales():
    retorno = None
    materiales = listar_materiales()
    retorno = jsonify(materiales), 200
    return retorno


@materiales_bp.route("/materiales", methods=["POST"])
@token_required
def post_materiales():
    retorno = None
    data = {
        "titulo": request.form.get("titulo"),
        "file": request.files.get("file")
    }
    
    errores, datos_validados = validar_subida_material(data)
    
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = guardar_material(datos_validados["titulo"], datos_validados["file"])
        
        if "error" in resultado:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = jsonify(resultado), 201
            
    return retorno


@materiales_bp.route("/materiales/<int:id_material>", methods=["DELETE"])
@token_required
def delete_materiales(id_material):
    retorno = None
    resultado = eliminar_material(id_material)
    
    if "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"], "description": "Verifique el ID del material."}]}), 404
        else:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
    else:
        retorno = "", 204
        
    return retorno
