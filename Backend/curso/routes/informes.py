from flask import Blueprint, jsonify, request, send_file
from io import BytesIO
from curso.services.informes import (
    informe_alumnos,
    informe_estadisticas,
    informe_equipos,
)

informes_bp = Blueprint("informes", __name__)


@informes_bp.route("/informes/alumnos", methods=["GET"])
def descargar_informe_alumnos():
    abandono_param = request.args.get("abandono")
    abandono = None
    if abandono_param is not None:
        if abandono_param.lower() in ("true", "1", "si", "sí"):
            abandono = True
        elif abandono_param.lower() in ("false", "0", "no"):
            abandono = False
        else:
            return jsonify({"error": "El parámetro 'abandono' debe ser true o false."}), 400

    try:
        pdf_bytes = informe_alumnos(abandono)
    except Exception as e:
        return jsonify({"error": f"Error al generar el informe: {str(e)}"}), 500

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="informe_alumnos.pdf",
    )


@informes_bp.route("/informes/estadisticas", methods=["GET"])
def descargar_informe_estadisticas():
    try:
        pdf_bytes = informe_estadisticas()
    except Exception as e:
        return jsonify({"error": f"Error al generar el informe: {str(e)}"}), 500

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="informe_estadisticas.pdf",
    )


@informes_bp.route("/informes/equipos", methods=["GET"])
def descargar_informe_equipos():
    try:
        pdf_bytes = informe_equipos()
    except Exception as e:
        return jsonify({"error": f"Error al generar el informe: {str(e)}"}), 500

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="informe_equipos.pdf",
    )
