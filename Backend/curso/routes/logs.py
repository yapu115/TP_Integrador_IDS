from flask import Blueprint, request, jsonify

from curso.utils.security import token_required

from curso.validators.logs import validar_crear_log

from curso.services.logs import (
    listar_logs,
    obtener_log_por_id,
    crear_log
)


logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/logs", methods=["GET"])
@token_required
def get_logs():
    usuario_id = request.args.get("usuario_id")
    accion = request.args.get("accion")
    fecha = request.args.get("fecha")

    resultado = listar_logs(usuario_id, accion, fecha)

    return jsonify(resultado), 200


@logs_bp.route("/logs/<int:id_log>", methods=["GET"])
@token_required
def get_log_por_id(id_log):
    resultado = obtener_log_por_id(id_log)

    if resultado is None:
        return jsonify({"error": "Log no encontrado"}), 404

    return jsonify(resultado), 200


@logs_bp.route("/logs", methods=["POST"])
@token_required
def post_log():
    data = request.get_json(silent=True) or {}

    errores, datos_validados = validar_crear_log(data)

    if errores:
        return jsonify({"errors": errores}), 400

    resultado = crear_log(datos_validados)

    return jsonify(resultado), 201