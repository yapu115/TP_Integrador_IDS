from flask import jsonify,request
from functools import wraps
from curso.services.logs import crear_log


def error_respuesta(mensaje,codigo_error):
    return jsonify({"error": mensaje}), codigo_error

def registrar_actividad(accion_nombre):
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            respuesta = f(*args, **kwargs)
            
            codigo_estado = respuesta[1]
                
            if codigo_estado in [200, 201,204]:
                
                try:
                    if codigo_estado == 204:
                        detalles_json = "Registro eliminado"
                    else:
                        detalles_json = request.get_data(as_text=True)
                        
                    usuario_info = getattr(request, 'usuario_actual', None)
                    usuario_real = usuario_info.get('username')

                    crear_log({
                        "usuario": usuario_real,  
                        "accion": accion_nombre,
                        "detalles": f"{detalles_json}"
                    })
                except Exception as e:
                    print(f" Error al guardar log: {e}") 
            return respuesta
        return decorada
    return decorador