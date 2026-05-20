from flask import request

def validar_get_alumnos():
    args = request.args
    
    # 1. Validar _limit
    if '_limit' in args:
        try:
            limit = int(args['_limit'])
            if limit < 1:
                return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _limit debe ser mayor a 0", "level": "error"}]}, 400
        except ValueError:
            return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _limit debe ser un número entero", "level": "error"}]}, 400

    # 2. Validar _offset
    if '_offset' in args:
        try:
            offset = int(args['_offset'])
            if offset < 0:
                return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _offset debe ser mayor o igual a 0", "level": "error"}]}, 400
        except ValueError:
            return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _offset debe ser un número entero", "level": "error"}]}, 400

    # 3. Validar abandono (debe ser true o false)
    if 'abandono' in args:
        if args['abandono'].lower() not in ['true', 'false']:
            return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro abandono debe ser true o false", "level": "error"}]}, 400
            
    return None

def validar_id_entero(id_url):
    try:
        id_int = int(id_url)
        if id_int <= 0:
            return None, {"errors": [{"code": "VALIDATION_ERROR", "message": "El ID debe ser mayor a 0", "level": "error"}]}, 400
        return id_int, None
    except ValueError:
        return None, {"errors": [{"code": "VALIDATION_ERROR", "message": "El ID debe ser un número entero", "level": "error"}]}, 400
