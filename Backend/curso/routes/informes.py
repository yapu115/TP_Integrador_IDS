from flask import Blueprint, jsonify, request, send_file
from io import BytesIO

from curso.utils.security import token_required
from curso.validators.informes import validar_abandono_informe
from curso.services.informes import (
    informe_alumnos,
    informe_estadisticas,
    informe_equipos,
)

informes_bp = Blueprint("informes", __name__)


def _respuesta_error_interno(detalle):
    return jsonify({
        "errors": [{
            "code": "INTERNAL_SERVER_ERROR",
            "message": "Error al generar el informe.",
            "level": "error",
            "description": detalle,
        }]
    }), 500


@informes_bp.route("/informes/alumnos", methods=["GET"])
@token_required
def descargar_informe_alumnos():
    abandono, error_validacion = validar_abandono_informe()
    if error_validacion:
        return jsonify(error_validacion[0]), error_validacion[1]

    try:
        pdf_bytes = informe_alumnos(abandono)
    except Exception as e:
        return _respuesta_error_interno(str(e))

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="informe_alumnos.pdf",
    )


@informes_bp.route("/informes/estadisticas", methods=["GET"])
@token_required
def descargar_informe_estadisticas():
    try:
        pdf_bytes = informe_estadisticas()
    except Exception as e:
        return _respuesta_error_interno(str(e))

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="informe_estadisticas.pdf",
    )


@informes_bp.route("/informes/equipos", methods=["GET"])
@token_required
def descargar_informe_equipos():
    try:
        pdf_bytes = informe_equipos()
    except Exception as e:
        return _respuesta_error_interno(str(e))

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="informe_equipos.pdf",
    )
