from flask import Blueprint, jsonify, request
from curso.validators.evaluaciones import validar_campos_evaluaciones, validar_evaluacion
from curso.services.evaluaciones import (
    crear_evaluacion_servicio,
    listar_evaluaciones_service,
    modificar_evaluacion_service,
    eliminar_evaluacion_service
)
from curso.utils.security import token_required
from curso.utils.utils import registrar_actividad

evaluacion_bp = Blueprint('evaluaciones', __name__)

@evaluacion_bp.route("/evaluaciones", methods=['GET'])
@token_required
def listar_evaluaciones_route():
    retorno = None
    try:
        evaluaciones = listar_evaluaciones_service()
        if evaluaciones is None:
            retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error al listar las evaluaciones."}]}), 500
        else:
            retorno = jsonify(evaluaciones), 200
    except Exception:
        retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error interno del servidor."}]}), 500
        
    return retorno
    
@evaluacion_bp.route("/evaluaciones", methods=['POST'])
@token_required
@registrar_actividad("CREACION_EVALUACION")
def crear_evaluacion_route():
    retorno = None
    data = request.get_json(silent=True) or {}

    errores = validar_campos_evaluaciones(data)
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        try:
            evaluacion = crear_evaluacion_servicio(data)
            if evaluacion is None:
                retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error en la base de datos."}]}), 500
            else:
                retorno = "", 201
        except Exception:
            retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error interno del servidor."}]}), 500
            
    return retorno

@evaluacion_bp.route("/evaluaciones/<int:id_evaluacion>", methods=['GET'])
@token_required
def mostrar_evaluacion_route(id_evaluacion):  
    retorno = None
    try:
        evaluacion = validar_evaluacion(id_evaluacion)
        if evaluacion is None:
            retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": "Evaluación no encontrada."}]}), 404
        else:
            retorno = jsonify(evaluacion), 200
    except Exception:
        retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error interno del servidor."}]}), 500
        
    return retorno

@evaluacion_bp.route("/evaluaciones/<int:id_evaluacion>", methods=['PUT'])
@token_required
@registrar_actividad("MODIFICAR_EVALUACION")
def modificar_evaluacion_route(id_evaluacion):
    retorno = None
    data = request.get_json(silent=True) or {}
    
    errores = validar_campos_evaluaciones(data)
    if errores:
        retorno = jsonify({"errors": errores}), 400
    else:
        try:
            evaluacion = validar_evaluacion(id_evaluacion)
            if evaluacion is None:
                retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": "Evaluación no encontrada."}]}), 404
            else:
                cambios = modificar_evaluacion_service(id_evaluacion, data)
                if cambios is None:
                    retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error al modificar."}]}), 500
                else:
                    retorno = "", 200
        except Exception:
            retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error interno del servidor."}]}), 500
            
    return retorno

@evaluacion_bp.route("/evaluaciones/<int:id_evaluacion>", methods=['DELETE'])
@token_required
@registrar_actividad("ELIMINAR_EVALUACION")
def eliminar_evaluacion_route(id_evaluacion):
    retorno = None
    try:
        evaluacion = validar_evaluacion(id_evaluacion)
        if evaluacion is None:
           retorno = jsonify({"errors": [{"code": "NOT_FOUND", "message": "Evaluación no encontrada."}]}), 404
        else:
            cambios = eliminar_evaluacion_service(id_evaluacion)
            if cambios is None:
                retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error al eliminar."}]}), 500
            else:
                retorno = "", 204
    except Exception:
        retorno = jsonify({"errors": [{"code": "INTERNAL_SERVER_ERROR", "message": "Error interno del servidor."}]}), 500    
        
    return retorno
