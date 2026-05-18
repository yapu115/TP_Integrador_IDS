from flask import Blueprint, jsonify, request
from curso.utils import error_respuesta
from curso.validators.evaluaciones import validar_evaluaciones,validar_campos_evaluaciones
from curso.services.evaluaciones import crear_evaluacion_servicio
evaluacion_bp= Blueprint('evaluaciones',__name__)

@evaluacion_bp.route("/evaluaciones",methods=['GET'])
def listar_evaluaciones():
    
    evaluaciones=validar_evaluaciones()
    try:
        if evaluaciones is None:
            return error_respuesta("No se encontraron evaluaciones",404)
        else:
            return jsonify({"status":"exitoso",
                            "message":"Mostrando evaluaciones"},evaluaciones),200
    except Exception:
        return error_respuesta("error interno del servidor",500)
    
@evaluacion_bp.route("/evaluaciones",methods=['POST'])
def crear_evaluacion():
    data = request.get_json()
    
    evaluacion=crear_evaluacion_servicio(data)
    campos=validar_campos_evaluaciones(data)
    if not campos:
        return error_respuesta("Todos los campos deben ser completados",400)
    try:
        if evaluacion is None:
            return error_respuesta("error en la base de datos",500)
    
        if evaluacion<1:
            return error_respuesta("No se realizaron cambios en la base de datos",204)
        
        return jsonify({"status":"exitoso",
                        "message":"Se agrego un recurso nuevo"})
    except Exception:
        return error_respuesta("error interno del servidor",500)
