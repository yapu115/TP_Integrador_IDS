from flask import request


def validar_abandono_informe():
    if 'abandono' not in request.args:
        return None, None

    valor = request.args['abandono'].lower()
    if valor == 'true':
        return True, None
    if valor == 'false':
        return False, None

    return None, (
        {"errors": [{
            "code": "VALIDATION_ERROR",
            "message": "El parámetro abandono debe ser true o false",
            "level": "error",
        }]},
        400,
    )
