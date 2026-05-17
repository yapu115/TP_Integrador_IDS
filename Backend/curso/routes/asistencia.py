from flask import Blueprint, request, jsonify

from curso.validators.asistencia import (
    validar_generar_qr,
    validar_registrar_asistencia
)

from curso.services.asistencia import (
    generar_qr_asistencia,
    registrar_asistencia,
    obtener_asistencias_por_alumno
)


asistencia_bp = Blueprint("asistencia", __name__)


@asistencia_bp.route("/asistencia/qr", methods=["POST"])
def generar_qr():
    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "El cuerpo de la petición debe ser JSON."
        }), 400

    errores, datos_validados = validar_generar_qr(data)

    if errores:
        return jsonify({
            "errores": errores
        }), 400

    resultado = generar_qr_asistencia(
        datos_validados["id_alumno"],
        datos_validados["fecha"]
    )

    if resultado is None:
        return jsonify({
            "error": "No existe un alumno con ese id."
        }), 404

    return jsonify(resultado), 200


@asistencia_bp.route("/asistencia/registrar", methods=["POST"])
def registrar():
    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "El cuerpo de la petición debe ser JSON."
        }), 400

    errores, datos_validados = validar_registrar_asistencia(data)

    if errores:
        return jsonify({
            "errores": errores
        }), 400

    resultado = registrar_asistencia(
        datos_validados["id_alumno"],
        datos_validados["fecha"],
        datos_validados["codigo_qr"],
        datos_validados["estado"]
    )

    if not resultado["ok"]:
        return jsonify({
            "error": resultado["mensaje"]
        }), resultado["status"]

    return jsonify({
        "mensaje": resultado["mensaje"],
        "asistencia": resultado["data"]
    }), resultado["status"]


@asistencia_bp.route("/alumnos/<int:id_alumno>/asistencias", methods=["GET"])
def listar_asistencias_alumno(id_alumno):
    asistencias = obtener_asistencias_por_alumno(id_alumno)

    if asistencias is None:
        return jsonify({
            "error": "No existe un alumno con ese id."
        }), 404

    return jsonify({
        "id_alumno": id_alumno,
        "asistencias": asistencias
    }), 200