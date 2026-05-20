from flask import jsonify
def error_respuesta(mensaje,codigo_error):
    return jsonify({"error": mensaje}), codigo_error


