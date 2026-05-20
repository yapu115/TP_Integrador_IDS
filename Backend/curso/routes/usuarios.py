from flask import Blueprint, request, jsonify
from curso.validators.usuarios import validar_login, validar_crear_usuario, validar_actualizar_usuario
from curso.services.usuarios import login_usuario, crear_usuario, listar_usuarios, actualizar_usuario, obtener_usuario, eliminar_usuario
from curso.utils.security import token_required

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios/login", methods=["POST"])
def login():
    """
    Ruta pública para autenticarse y obtener el JWT.
    """
    data = request.get_json()
    retorno = None

    if not data:
        retorno = jsonify({
            "errors": [{
                "code": "VALIDATION_ERROR", 
                "message": "El cuerpo de la petición debe ser JSON.",
                "description": "Asegúrese de enviar los datos en formato JSON."
            }]
        }), 400
        
    if not retorno:
        errores, datos_validados = validar_login(data)
        if errores:
            retorno = jsonify({"errors": errores}), 400
            
    if not retorno:
        resultado = login_usuario(datos_validados["username"], datos_validados["password"])
        if "error" in resultado:
            retorno = jsonify({
                "errors": [{
                    "code": resultado["error"], 
                    "message": resultado["mensaje"],
                    "description": "Verifique sus credenciales e intente nuevamente."
                }]
            }), 401
        else:
            retorno = jsonify(resultado), 200
            
    return retorno


@usuarios_bp.route("/usuarios", methods=["POST"])
@token_required
def post_usuario():
    """
    Crea un nuevo usuario en el sistema.
    Ruta protegida, requiere enviar el JWT en el header.
    """
    data = request.get_json()
    retorno = None
    
    if not data:
        retorno = jsonify({
            "errors": [{
                "code": "VALIDATION_ERROR", 
                "message": "El cuerpo de la petición debe ser JSON.",
                "description": "Asegúrese de enviar los datos en formato JSON."
            }]
        }), 400
        
    if not retorno:
        errores, datos_validados = validar_crear_usuario(data)
        if errores:
            retorno = jsonify({"errors": errores}), 400
            
    if not retorno:
        resultado = crear_usuario(datos_validados)
        if "error" in resultado:
            retorno = jsonify({
                "errors": [{
                    "code": resultado["error"], 
                    "message": resultado["mensaje"],
                    "description": "Por favor elija otro nombre de usuario o correo."
                }]
            }), 409
        else:
            retorno = jsonify(resultado), 201
            
    return retorno

@usuarios_bp.route("/usuarios", methods=["GET"])
@token_required
def get_usuarios():
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)
    retorno = None
    

    resultado = listar_usuarios(limit, offset)
    if "error" in resultado:
        retorno = jsonify({
            "errors": [{
                "code": resultado["error"], 
                "message": resultado["mensaje"],
                "description": "Error al obtener la lista de usuarios"
            }]
        }), 409
    else:
        retorno = jsonify(resultado), 200
            
    return retorno

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["PUT"])
@token_required
def put_usuario(id_usuario):
    data = request.get_json()
    retorno = None

    if not data:
        retorno = jsonify({
            "errors": [{
                "code": "VALIDATION_ERROR", 
                "message": "El cuerpo de la petición debe ser JSON.",
                "description": "Asegúrese de enviar los datos en formato JSON."
            }]
        }), 400
    
    if not retorno:
        errores, datos_validados = validar_actualizar_usuario(data)
        if errores:
            retorno = jsonify({"errors": errores}), 400
        
    if not retorno:
        resultado = actualizar_usuario(id_usuario, datos_validados)
        if "error" in resultado:
            if resultado["error"] == "NOT_FOUND":
                retorno = jsonify({
                    "errors": [{
                        "code": "NOT_FOUND",
                        "message": resultado["mensaje"],
                        "description": "El usuario a actualizar no existe."
                    }]
                }), 404
            else:
                retorno = jsonify({
                    "errors": [{
                        "code": resultado["error"], 
                        "message": resultado["mensaje"],
                        "description": "Por favor elija otro nombre de usuario o correo."
                    }]
                }), 409
        else:
            retorno = "", 204
    
    
    return retorno

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["GET"])
@token_required
def get_usuario(id_usuario):
    usuario = obtener_usuario(id_usuario)
    
    if not usuario:
        return jsonify({
            "errors": [{
                "code": "NOT_FOUND", 
                "message": "Usuario no encontrado.",
                "description": f"No existe un usuario con el ID {id_usuario}."
            }]
        }), 404
        
    return jsonify(usuario), 200

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
@token_required
def delete_usuario(id_usuario):
    resultado = eliminar_usuario(id_usuario)
    
    if "error" in resultado:
        if resultado["error"] == "NOT_FOUND":
            return jsonify({
                "errors": [{
                    "code": "NOT_FOUND", 
                    "message": resultado["mensaje"],
                    "description": f"No existe un usuario con el ID {id_usuario}."
                }]
            }), 404
        else:
            return jsonify({
                "errors": [{
                    "code": resultado["error"], 
                    "message": resultado["mensaje"],
                    "description": "Error al eliminar el usuario."
                }]
            }), 500
            
    return "", 204
