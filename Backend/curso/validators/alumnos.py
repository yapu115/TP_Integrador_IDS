import re
from flask import request

COLUMNAS_CSV = {'legajo', 'nombre', 'apellido', 'email'}


def validar_get_alumnos():
    args = request.args

    if '_limit' in args:
        try:
            limit = int(args['_limit'])
            if limit < 1:
                return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _limit debe ser mayor a 0", "level": "error"}]}, 400
        except ValueError:
            return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _limit debe ser un número entero", "level": "error"}]}, 400

    if '_offset' in args:
        try:
            offset = int(args['_offset'])
            if offset < 0:
                return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _offset debe ser mayor o igual a 0", "level": "error"}]}, 400
        except ValueError:
            return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro _offset debe ser un número entero", "level": "error"}]}, 400

    if 'abandono' in args:
        if args['abandono'].lower() not in ['true', 'false']:
            return {"errors": [{"code": "VALIDATION_ERROR", "message": "El parámetro abandono debe ser true o false", "level": "error"}]}, 400

    return None


def validar_crear_alumno(data):
    errores = []

    if not data:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El cuerpo de la petición debe ser JSON.",
            "level": "error",
            "description": "Asegúrese de enviar los datos en formato JSON."
        })
        return errores, None

    legajo = data.get('legajo')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')

    if legajo is None or str(legajo).strip() == '':
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo legajo.",
            "level": "error"
        })
    if not nombre or not str(nombre).strip():
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo nombre.",
            "level": "error"
        })
    if not apellido or not str(apellido).strip():
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo apellido.",
            "level": "error"
        })
    if not email or not str(email).strip():
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Falta el campo email.",
            "level": "error"
        })
    elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', str(email).strip()):
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El email no tiene un formato válido.",
            "level": "error"
        })

    if errores:
        return errores, None

    return [], {
        'legajo': str(legajo).strip(),
        'nombre': str(nombre).strip(),
        'apellido': str(apellido).strip(),
        'email': str(email).strip()
    }


def validar_actualizar_alumno(data):
    errores = []

    if not data:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El cuerpo de la petición debe ser JSON.",
            "level": "error"
        })
        return errores, None

    campos_permitidos = {'nombre', 'apellido', 'email', 'abandono'}
    datos = {}

    for campo in campos_permitidos:
        if campo in data:
            datos[campo] = data[campo]

    if not datos:
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "Debe enviar al menos un campo para actualizar.",
            "level": "error"
        })
        return errores, None

    if 'nombre' in datos and (not datos['nombre'] or not str(datos['nombre']).strip()):
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El campo nombre no puede estar vacío.",
            "level": "error"
        })
    if 'apellido' in datos and (not datos['apellido'] or not str(datos['apellido']).strip()):
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El campo apellido no puede estar vacío.",
            "level": "error"
        })
    if 'email' in datos:
        email = str(datos['email']).strip()
        if not email:
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "El campo email no puede estar vacío.",
                "level": "error"
            })
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errores.append({
                "code": "VALIDATION_ERROR",
                "message": "El email no tiene un formato válido.",
                "level": "error"
            })
        else:
            datos['email'] = email
    if 'abandono' in datos and not isinstance(datos['abandono'], bool):
        errores.append({
            "code": "VALIDATION_ERROR",
            "message": "El campo abandono debe ser true o false.",
            "level": "error"
        })

    if errores:
        return errores, None

    if 'nombre' in datos:
        datos['nombre'] = str(datos['nombre']).strip()
    if 'apellido' in datos:
        datos['apellido'] = str(datos['apellido']).strip()

    return [], datos


def validar_csv_import(rows):
    if not rows:
        return [{
            "code": "VALIDATION_ERROR",
            "message": "El archivo CSV está vacío.",
            "level": "error"
        }], None

    if not COLUMNAS_CSV.issubset(rows[0].keys()):
        faltantes = COLUMNAS_CSV - set(rows[0].keys())
        return [{
            "code": "VALIDATION_ERROR",
            "message": f"Faltan columnas en el CSV: {', '.join(sorted(faltantes))}",
            "level": "error"
        }], None

    filas_validadas = []
    legajos_vistos = set()
    for i, row in enumerate(rows, start=2):
        legajo = (row.get('legajo') or '').strip()
        nombre = (row.get('nombre') or '').strip()
        apellido = (row.get('apellido') or '').strip()
        email = (row.get('email') or '').strip()

        if not all([legajo, nombre, apellido, email]):
            return [{
                "code": "VALIDATION_ERROR",
                "message": f"Fila {i}: todos los campos son obligatorios.",
                "level": "error"
            }], None

        if legajo in legajos_vistos:
            return [{
                "code": "VALIDATION_ERROR",
                "message": f"Fila {i}: el legajo {legajo} esta duplicado dentro del archivo.",
                "level": "error"
            }], None

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return [{
                "code": "VALIDATION_ERROR",
                "message": f"Fila {i}: el email no tiene un formato valido.",
                "level": "error"
            }], None

        legajos_vistos.add(legajo)
        filas_validadas.append({
            'legajo': legajo,
            'nombre': nombre,
            'apellido': apellido,
            'email': email
        })

    return [], filas_validadas
