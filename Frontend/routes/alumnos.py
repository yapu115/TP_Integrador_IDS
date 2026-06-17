import csv
from io import StringIO
from urllib.parse import urlencode

from flask import Blueprint, Response, flash, render_template, request, session, redirect, url_for
from utils.auth import login_required
from services.api_client import delete_json, get_json, patch_json, post_json, post_multipart_file

alumnos_bp = Blueprint("alumnos", __name__)


def primer_mensaje_error(data, fallback="Ocurrio un error."):
    errores = data.get("errors", []) if isinstance(data, dict) else []
    if errores:
        return errores[0].get("message", fallback)
    return data.get("message", fallback) if isinstance(data, dict) else fallback


def aplicar_filtros(alumnos_lista, filtros):
    nombre = filtros.get("nombre", "").lower()
    apellido = filtros.get("apellido", "").lower()
    legajo = filtros.get("legajo", "").lower()
    estado = filtros.get("estado", "")

    filtrados = []
    for alumno in alumnos_lista:
        if nombre and nombre not in str(alumno.get("nombre", "")).lower():
            continue
        if apellido and apellido not in str(alumno.get("apellido", "")).lower():
            continue
        if legajo and legajo not in str(alumno.get("legajo", "")).lower():
            continue
        if estado == "activo" and alumno.get("abandono"):
            continue
        if estado == "abandono" and not alumno.get("abandono"):
            continue
        filtrados.append(alumno)

    return filtrados


@alumnos_bp.route("/alumnos", methods=["GET", "POST"])
@login_required
def alumnos():
    token = session.get("token")
    curso_id = session.get("curso_id")
    error = None
    exito = None
    importados = request.args.get("importados")
    if importados is not None:
        exito = f"Importacion CSV completada. Registros procesados: {importados}."

    if request.method == "POST":
        accion = request.form.get("accion", "crear")

        if accion == "crear":
            body = {
                "legajo": request.form.get("legajo", "").strip(),
                "nombre": request.form.get("nombre", "").strip(),
                "apellido": request.form.get("apellido", "").strip(),
                "email": request.form.get("email", "").strip(),
            }

            if not all(body.values()):
                error = "Todos los campos del alumno son obligatorios."
            else:
                status, data = post_json(f"/alumnos?curso_id={curso_id}", body, token=token)
                if status == 201:
                    exito = "Alumno agregado correctamente."
                elif status in (401, 403):
                    session.clear()
                    return redirect(url_for("auth.login"))
                else:
                    error = primer_mensaje_error(data, "Error al agregar el alumno.")

        elif accion == "editar":
            alumno_id = request.form.get("alumno_id")
            body = {
                "nombre": request.form.get("nombre", "").strip(),
                "apellido": request.form.get("apellido", "").strip(),
                "email": request.form.get("email", "").strip(),
            }

            if not alumno_id or not all(body.values()):
                error = "Nombre, apellido y email son obligatorios para editar."
            else:
                status, data = patch_json(f"/alumnos/{alumno_id}", body, token=token)
                if status == 200:
                    exito = "Alumno actualizado correctamente."
                elif status in (401, 403):
                    session.clear()
                    return redirect(url_for("auth.login"))
                else:
                    error = primer_mensaje_error(data, "Error al actualizar el alumno.")

        elif accion == "estado":
            alumno_id = request.form.get("alumno_id")
            abandono = request.form.get("abandono") == "true"
            status, data = patch_json(f"/alumnos/{alumno_id}", {"abandono": abandono}, token=token)
            if status == 200:
                exito = "Estado del alumno actualizado."
            elif status in (401, 403):
                session.clear()
                return redirect(url_for("auth.login"))
            else:
                error = primer_mensaje_error(data, "Error al actualizar el estado.")

        elif accion == "eliminar":
            alumno_id = request.form.get("alumno_id")
            status, data = delete_json(f"/alumnos/{alumno_id}", token=token)
            if status == 204:
                exito = "Alumno eliminado correctamente."
            elif status in (401, 403):
                session.clear()
                return redirect(url_for("auth.login"))
            else:
                error = primer_mensaje_error(data, "Error al eliminar el alumno.")
        else:
            error = "Accion no reconocida."

        if error:
            flash(error, "error")
        elif exito:
            flash(exito, "success")
        return redirect(url_for("alumnos.alumnos"))

    filtros = {
        "nombre": request.args.get("nombre", "").strip(),
        "apellido": request.args.get("apellido", "").strip(),
        "legajo": request.args.get("legajo", "").strip(),
        "estado": request.args.get("estado", "").strip(),
    }
    params = {
        "curso_id": curso_id,
        "_limit": 100,
    }
    if filtros["nombre"]:
        params["nombre"] = filtros["nombre"]
    if filtros["apellido"]:
        params["apellido"] = filtros["apellido"]
    if filtros["legajo"]:
        params["legajo"] = filtros["legajo"]
    if filtros["estado"] == "activo":
        params["abandono"] = "false"
    elif filtros["estado"] == "abandono":
        params["abandono"] = "true"

    status, data = get_json(f"/alumnos?{urlencode(params)}", token=token)

    if status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))

    alumnos_lista = []
    if status == 200 and isinstance(data, dict):
        alumnos_lista = data.get("alumnos", [])
    elif status not in (200, 204) and not error:
        error = primer_mensaje_error(data, "No se pudieron cargar los alumnos.")

    alumnos_lista = aplicar_filtros(alumnos_lista, filtros)

    return render_template(
        "alumnos.html",
        alumnos=alumnos_lista,
        error=error,
        exito=exito,
        filtros=filtros,
    )


@alumnos_bp.route("/alumnos/importar", methods=["POST"])
@login_required
def importar_alumnos():
    token = session.get("token")
    curso_id = session.get("curso_id")
    archivo = request.files.get("file")

    if not archivo:
        flash("Debe seleccionar un archivo CSV.", "error")
        return redirect(url_for("alumnos.alumnos"))

    status, data = post_multipart_file(
        f"/alumnos/importar?curso_id={curso_id}",
        "file",
        archivo,
        token=token,
    )

    if status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))

    if status == 200:
        procesados = data.get("procesados", 0) if isinstance(data, dict) else 0
        return redirect(url_for("alumnos.alumnos", importados=procesados))

    error = primer_mensaje_error(data, "Error al importar alumnos.")
    flash(error, "error")
    return redirect(url_for("alumnos.alumnos"))


@alumnos_bp.route("/alumnos/exportar", methods=["GET"])
@login_required
def exportar_alumnos():
    token = session.get("token")
    curso_id = session.get("curso_id")

    filtros = {
        "nombre": request.args.get("nombre", "").strip(),
        "apellido": request.args.get("apellido", "").strip(),
        "legajo": request.args.get("legajo", "").strip(),
        "estado": request.args.get("estado", "").strip(),
    }
    params = {
        "curso_id": curso_id,
        "_limit": 10000,
    }
    if filtros["nombre"]:
        params["nombre"] = filtros["nombre"]
    if filtros["apellido"]:
        params["apellido"] = filtros["apellido"]
    if filtros["legajo"]:
        params["legajo"] = filtros["legajo"]
    if filtros["estado"] == "activo":
        params["abandono"] = "false"
    elif filtros["estado"] == "abandono":
        params["abandono"] = "true"

    status, data = get_json(f"/alumnos?{urlencode(params)}", token=token)

    if status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))

    alumnos_lista = data.get("alumnos", []) if status == 200 and isinstance(data, dict) else []
    alumnos_lista = aplicar_filtros(alumnos_lista, filtros)

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["legajo", "nombre", "apellido", "email", "abandono"])

    for alumno in alumnos_lista:
        writer.writerow([
            alumno.get("legajo", ""),
            alumno.get("nombre", ""),
            alumno.get("apellido", ""),
            alumno.get("email", ""),
            "true" if alumno.get("abandono") else "false",
        ])

    filename = f"alumnos_curso_{curso_id}.csv"
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
