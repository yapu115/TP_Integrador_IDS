from flask import Blueprint, request, jsonify
from curso.utils.security import token_required
from datetime import date
from curso.db import mysql

from curso.validators.asistencia import (
    validar_generar_qr,
    validar_enviar_qr,
    validar_enviar_qr_curso,
    validar_registrar_asistencia
)

from curso.services.asistencia import (
    generar_qr_asistencia,
    enviar_qr_asistencia,
    enviar_qr_asistencia_curso,
    registrar_asistencia,
    obtener_asistencias_por_alumno,
    obtener_envios_qr_curso,
    obtener_estado_asistencia_hoy,
    crear_clase_obligatoria,
    obtener_clases_obligatorias,
    reprogramar_clase_obligatoria
)


asistencia_bp = Blueprint("asistencia", __name__)


@asistencia_bp.route("/asistencia/qr", methods=["POST"])
#@token_required
def generar_qr():
    retorno = None
    data = request.get_json(silent=True) or {}

    errores, datos_validados = validar_generar_qr(data)

    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = generar_qr_asistencia(datos_validados["id_alumno"], datos_validados["fecha"])

        if "error" in resultado:
            if resultado["error"] == "NOT_FOUND":
                retorno = jsonify({
                    "errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"], "description": "Verifique el ID del alumno."}]
                }), 404
            else:
                retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = jsonify(resultado), 200

    return retorno


@asistencia_bp.route("/asistencia/qr/enviar", methods=["POST"])
#@token_required
def enviar_qr():
    retorno = None
    data = request.get_json(silent=True) or {}

    errores, datos_validados = validar_enviar_qr(data)

    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = enviar_qr_asistencia(datos_validados["id_alumno"], datos_validados["fecha"])

        if "error" in resultado:
            if resultado["error"] == "NOT_FOUND":
                retorno = jsonify({
                    "errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"], "description": "Verifique el ID del alumno."}]
                }), 404
            else:
                retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = jsonify(resultado), 200

    return retorno


@asistencia_bp.route("/asistencia/qr/enviar/todos", methods=["POST"])
#@token_required
def enviar_qr_todos():
    retorno = None
    data = request.get_json(silent=True) or {}

    errores, datos_validados = validar_enviar_qr_curso(data)

    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = enviar_qr_asistencia_curso(datos_validados["curso_id"], datos_validados["fecha"])

        if "error" in resultado:
            if resultado["error"] == "NOT_FOUND":
                retorno = jsonify({
                    "errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"], "description": "Verifique que el curso tenga alumnos activos."}]
                }), 404
            else:
                retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = jsonify(resultado), 200

    return retorno


@asistencia_bp.route("/asistencia/envios", methods=["GET"])
#@token_required
def listar_envios_qr():
    curso_id = request.args.get("curso_id", type=int)
    fecha = request.args.get("fecha")

    if not curso_id or not fecha:
        return jsonify({
            "errors": [{"code": "BAD_REQUEST", "message": "Se requieren curso_id y fecha."}]
        }), 400

    envios = obtener_envios_qr_curso(curso_id, fecha)
    return jsonify({"envios": envios}), 200


@asistencia_bp.route("/asistencia/registrar", methods=["GET"])
def registrar_desde_qr():
    codigo_qr = request.args.get("codigo_qr")

    if not codigo_qr:
        return """
        <html>
            <body style="font-family: Arial; text-align: center; padding: 40px;">
                <h2>Error al registrar asistencia</h2>
                <p>No se recibió ningún código QR.</p>
            </body>
        </html>
        """, 400

    try:
        resultado = registrar_asistencia(codigo_qr)

        print("CODIGO QR RECIBIDO:", codigo_qr)
        print("RESULTADO:", resultado)

        if resultado is None:
            return """
            <html>
                <body style="font-family: Arial; text-align: center; padding: 40px;">
                    <h2>Error interno</h2>
                    <p>La función registrar_asistencia no devolvió ninguna respuesta.</p>
                </body>
            </html>
            """, 500

        if "error" in resultado:
            return f"""
            <html>
                <body style="font-family: Arial; text-align: center; padding: 40px;">
                    <h2>No se pudo registrar la asistencia</h2>
                    <p>{resultado.get("mensaje", "Error desconocido")}</p>
                </body>
            </html>
            """, 400

        return f"""
        <html>
            <body style="font-family: Arial; background-color: #f4f4f4; padding: 40px;">
                <div style="max-width: 500px; margin: auto; background-color: white; padding: 30px; border-radius: 10px; text-align: center;">
                    <h2 style="color: #263642;">Asistencia registrada correctamente</h2>
                    <p>{resultado.get("mensaje", "La asistencia fue registrada.")}</p>
                    <p><strong>Alumno ID:</strong> {resultado.get("id_alumno", "No disponible")}</p>
                    <p><strong>Fecha:</strong> {resultado.get("fecha", "No disponible")}</p>
                </div>
            </body>
        </html>
        """, 200

    except Exception as exc:
        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; padding: 40px;">
                <h2>Error interno del servidor</h2>
                <p>{exc}</p>
            </body>
        </html>
        """, 500

@asistencia_bp.route("/asistencia/registrar", methods=["POST"])
#@token_required
def registrar():
    retorno = None
    data = request.get_json(silent=True) or {}

    errores, datos_validados = validar_registrar_asistencia(data)

    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        resultado = registrar_asistencia(datos_validados["codigo_qr"])

        if "error" in resultado:
            if resultado["error"] == "BAD_REQUEST":
                retorno = jsonify({"errors": [{"code": "BAD_REQUEST", "message": resultado["mensaje"]}]}), 400
            elif resultado["error"] == "NOT_FOUND":
                retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": resultado["mensaje"]}]}), 404
            else:
                retorno = jsonify({"errors": [{"code": resultado["error"], "message": resultado["mensaje"]}]}), 500
        else:
            retorno = "", 204

    return retorno


@asistencia_bp.route("/asistencia/clases", methods=["GET"])
def obtener_clases():
    resultado = obtener_clases_obligatorias()

    if isinstance(resultado, dict) and "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200

@asistencia_bp.route("/asistencia/crear-clase", methods=["POST"])
def crear_clase():
    
    fecha = request.form.get('fecha')
    nombre_clase = request.form.get('nombre_clase')

    if not fecha or not nombre_clase:
        return jsonify({
            "error": "Debe completar la fecha y el nombre de la clase."
        }), 400

    resultado = crear_clase_obligatoria(fecha, nombre_clase)

    if "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200

@asistencia_bp.route("/asistencia/reprogramar-clase", methods=["POST"])
def reprogramar_clase():
    data = request.get_json(silent=True)

    if data is None:
        data = request.form

    fecha_actual = data.get("fecha_actual")
    nombre_clase = data.get("nombre_clase")
    nueva_fecha = data.get("nueva_fecha")

    if not fecha_actual or not nombre_clase or not nueva_fecha:
        return jsonify({
            "error": "Faltan datos para reprogramar la clase."
        }), 400

    resultado = reprogramar_clase_obligatoria(
        fecha_actual,
        nombre_clase,
        nueva_fecha
    )

    if isinstance(resultado, dict) and "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200