from flask import Blueprint, request, jsonify
from curso.utils.security import token_required, role_required
from curso.validators.materiales import validar_subida_material
from curso.services.cursos import curso_existe
from curso.services.materiales import listar_materiales, guardar_material, eliminar_material

materiales_bp = Blueprint("materiales", __name__)


def _get_curso_id():
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


@materiales_bp.route("/materiales", methods=["GET"])
@token_required
def get_materiales():
    curso_id, error = _get_curso_id()
    if error:
        return error

    materiales = listar_materiales(curso_id)
    retorno = jsonify(materiales), 200
    return retorno


@materiales_bp.route("/materiales", methods=["POST"])
@token_required
@role_required("admin")
def post_materiales():
    curso_id, error = _get_curso_id()
    if error:
        return error

    if not request.is_json:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Se requiere JSON."}]}), 400

    data = {
        "titulo": request.json.get("titulo"),
        "url_archivo": request.json.get("url_archivo")
    }

    errores, datos_validados = validar_subida_material(data)

    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = guardar_material(datos_validados["titulo"], datos_validados["url_archivo"], curso_id)
        if "error" in resultado:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = jsonify(resultado), 201

    return retorno


@materiales_bp.route("/materiales/<int:id_material>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete_materiales(id_material):
    
    resultado = eliminar_material(id_material)

    if "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
        else:
            retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
    else:
        retorno = "", 204

    return retorno
