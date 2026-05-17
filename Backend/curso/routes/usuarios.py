from flask import Blueprint, request, jsonify
from curso.validators.usuarios import validar_login
from curso.services.usuarios import login_usuario

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