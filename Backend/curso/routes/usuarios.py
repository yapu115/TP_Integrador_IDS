from flask import Blueprint, request, jsonify
from curso.validators.usuarios import validar_login, validar_crear_usuario
from curso.services.usuarios import login_usuario, crear_usuario
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