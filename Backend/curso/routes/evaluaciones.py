from flask import Blueprint, jsonify, request
from curso.utils import error_respuesta
from curso.validators.evaluaciones import validar_campos_evaluaciones,validar_evaluacion
from curso.services.evaluaciones import crear_evaluacion_servicio,listar_evaluaciones_service,modificar_evaluacion_service,eliminar_evaluacion_service
evaluacion_bp= Blueprint('evaluaciones',__name__)

@evaluacion_bp.route("/evaluaciones",methods=['GET'])
def listar_evaluaciones_route():
    
    evaluaciones=listar_evaluaciones_service()
    try:
        if evaluaciones is None:
            return error_respuesta("No se encontraron evaluaciones",404)
        else:
            return jsonify({"status":"exitoso",
                            "message":"Mostrando evaluaciones"},evaluaciones),200
    except Exception:
        return error_respuesta("error interno del servidor",500)
    
@evaluacion_bp.route("/evaluaciones",methods=['POST'])
def crear_evaluacion_route():
    data = request.get_json()

    campos=validar_campos_evaluaciones(data)
    if not campos:
        return error_respuesta("Todos los campos deben ser completados",400)
    try:
        evaluacion=crear_evaluacion_servicio(data)
        if evaluacion is None:
            return error_respuesta("error en la base de datos",500)
    
        if evaluacion<1:
            return error_respuesta("No se realizaron cambios en la base de datos",204)
        
        return jsonify({"status":"exitoso",
                        "message":"Se agrego un recurso nuevo"})
    except Exception:
        return error_respuesta("error interno del servidor",500)

@evaluacion_bp.route("/evaluaciones/<int:id_evaluacion>",methods=['GET'])
def mostrar_evaluacion_route(id_evaluacion):  
    try:
        evaluacion=validar_evaluacion(id_evaluacion)
        if evaluacion is None:
            return error_respuesta("No se econtro la evaluacion",404)
        else:
            return jsonify({"status":"exitoso",
                            "message":"mostrando evaluacion"},[evaluacion]),200
    except Exception:
        return error_respuesta("error interno del servidor",500)

@evaluacion_bp.route("/evaluaciones/<int:id_evaluacion>",methods=['PUT'])
def modificar_evaluacion_route(id_evaluacion):
    data = request.get_json()
    try:
        evaluacion=validar_evaluacion(id_evaluacion)
        
        if evaluacion is None:
            return error_respuesta("Evaluacion no encontrada o id invalido",404)
        
        cambios=modificar_evaluacion_service(id_evaluacion,data)
        if cambios <1:
            return error_respuesta("No se encontraron evaluaciones",204)
        else:
            return jsonify({"status":"exitoso",
                            "message":"Cambios realizados"}),200
    except Exception:
        return error_respuesta("error interno del servidor",500)

@evaluacion_bp.route("/evaluaciones/<int:id_evaluacion>",methods=['DELETE'])
def eliminar_evaluacion_route(id_evaluacion):
    try:
        evaluacion=validar_evaluacion(id_evaluacion)

        if evaluacion is None:
           return error_respuesta("No se econtro la evaluacion o el id es invalido",404)
        
        cambios=eliminar_evaluacion_service(id_evaluacion)
        if cambios<1:
            return error_respuesta("No se pudo eliminar la evaluacion",204)
        else:
            return jsonify({"status":"exitoso",
                            "message":"Cambios realizados"}),200
    except Exception:
        return error_respuesta("error interno del servidor",500)    
