from flask import Blueprint, jsonify, request
from curso.utils import error_respuesta
from curso.validators.evaluaciones import validar_campos_evaluaciones,validar_evaluacion
from curso.services.evaluaciones import crear_evaluacion_servicio,listar_evaluaciones_service,modificar_evaluacion_service,eliminar_evaluacion_service
evaluacion_bp= Blueprint('evaluaciones',__name__)

@evaluacion_bp.route("/evaluaciones",methods=['GET'])
def listar_evaluaciones_route():
    try:
        #lista toda la tabla tipos_evaluacion
        evaluaciones=listar_evaluaciones_service()
        if evaluaciones is None:
            return error_respuesta("No se encontraron evaluaciones",404)
        else:
            return jsonify({"status":"exitoso",
                            "message":"Mostrando evaluaciones"},evaluaciones),200
    except Exception:
        return error_respuesta("error interno del servidor",500)
    
@evaluacion_bp.route("/evaluaciones",methods=['POST'])
def crear_evaluacion_route():
    #guarda la request del servidor en data, luego la envia a una funcion para validar que sea correcta
    data = request.get_json()

    campos=validar_campos_evaluaciones(data)
    if not campos:
        return error_respuesta("Todos los campos deben ser completados",400)
    try:
        #envia la request a una funcion para crear el nuevo recurso
        evaluacion=crear_evaluacion_servicio(data)
        #la funcion devuelve la cantidad de cambios hechos en la base de datos
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
        #envia la id obtenida del endpoint a una funcion para que valide si existe y la trae
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
    #guarda la request del servidor en data, luego la envia a una funcion para validar que sea correcta 
    campos=validar_campos_evaluaciones(data)
    if not campos:
        return error_respuesta("Todos los campos deben ser completados",400)
    try:

        evaluacion=validar_evaluacion(id_evaluacion)
        #valida la id, devuelve None si no se encontro la id o si es invalido
        if evaluacion is None:
            return error_respuesta("Evaluacion no encontrada o id invalido",404)
        
        cambios=modificar_evaluacion_service(id_evaluacion,data)
        #se le pasa a una funcion el id que se va a modificar y la request con los cambios a realizar
        #devuelve la cantidad de cambios hechos en la base de datos
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
        #comprueba la existencia de ese id en la base de datos
        if evaluacion is None:
           return error_respuesta("No se econtro la evaluacion o el id es invalido",404)
        
        cambios=eliminar_evaluacion_service(id_evaluacion)
        #envia la id a una funcion para que sea eliminida, devuelve los cambios hechos en la base de datos
        if cambios<1:
            return error_respuesta("No se pudo eliminar la evaluacion",204)
        else:
            return jsonify({"status":"exitoso",
                            "message":"Cambios realizados"}),200
    except Exception:
        return error_respuesta("error interno del servidor",500)    
