from datetime import date

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from services.api_client import get_json, post_json
from utils.auth import login_required

asistencia_bp = Blueprint("asistencia", __name__)


def primer_mensaje_error(data, fallback="Ocurrio un error."):
    errores = data.get("errors", []) if isinstance(data, dict) else []
    if errores:
        return errores[0].get("message", fallback)
    return data.get("mensaje", fallback) if isinstance(data, dict) else fallback


def _curso_actual():
    curso_id = session.get("curso_id") or 1
    session["curso_id"] = curso_id
    return curso_id


def _cargar_alumnos(token, curso_id):
    status, data = get_json(f"/asistencia/tabla?curso_id={curso_id}", token=token)
    alumnos = []

    if status == 200 and isinstance(data, dict):
        for alumno in data.get("alumnos", []):
            estado = alumno.get("estado", "pendiente")
            alumnos.append({
                "id": alumno.get("id") or alumno.get("padron") or alumno.get("id_alumno"),
                "legajo": alumno.get("legajo"),
                "nombre": alumno.get("nombre"),
                "apellido": alumno.get("apellido"),
                "email": alumno.get("email"),
                "estado_asistencia": "Presente" if estado == "presente" else "Pendiente",
                "condicion": alumno.get("condicion", "Sin definir"),
            })

    return status, data, alumnos


def _cargar_clases(token):
    status, data = get_json("/asistencia/clases", token=token)
    if status != 200:
        return status, data, []
    if isinstance(data, list):
        return status, data, data
    if isinstance(data, dict):
        return status, data, data.get("clases", [])
    return status, data, []


@asistencia_bp.route("/asistencia", methods=["GET"])
@login_required
def asistencia():
    token = session.get("token")
    curso_id = _curso_actual()
    fecha_hoy = date.today().strftime("%Y-%m-%d")

    status, data, alumnos = _cargar_alumnos(token, curso_id)
    if status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))
    if status != 200:
        flash(primer_mensaje_error(data, "No se pudo cargar la asistencia."), "error")

    status_clases, data_clases, clases = _cargar_clases(token)
    if status_clases in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))
    if status_clases != 200:
        flash(primer_mensaje_error(data_clases, "No se pudieron cargar las clases obligatorias."), "error")

    clase_hoy = None
    for clase in clases:
        if str(clase.get("fecha"))[:10] == fecha_hoy:
            clase_hoy = clase
            break

    return render_template(
        "asistencia.html",
        alumnos=alumnos,
        fecha_hoy=fecha_hoy,
        historial=[],
        clases=clases,
        hay_clase_hoy=clase_hoy is not None,
        clase_hoy=clase_hoy,
    )


@asistencia_bp.route("/reprogramar-clase", methods=["POST"])
@login_required
def reprogramar_clase():
    token = session.get("token")
    clase_seleccionada = request.form.get("clase_seleccionada")
    nueva_fecha = request.form.get("nueva_fecha")

    if not clase_seleccionada:
        flash("Selecciona una clase para reprogramar.", "error")
        return redirect(url_for("asistencia.asistencia"))

    if not nueva_fecha:
        flash("Selecciona la nueva fecha.", "error")
        return redirect(url_for("asistencia.asistencia"))

    partes = clase_seleccionada.split("|", 1)
    if len(partes) != 2:
        flash("La clase seleccionada no tiene un formato valido.", "error")
        return redirect(url_for("asistencia.asistencia"))

    status, data = post_json(
        "/asistencia/reprogramar-clase",
        {
            "fecha_actual": partes[0],
            "nombre_clase": partes[1],
            "nueva_fecha": nueva_fecha,
        },
        token=token,
    )

    if status == 200:
        flash("Clase reprogramada correctamente.", "success")
    else:
        flash(primer_mensaje_error(data, "No se pudo reprogramar la clase."), "error")

    return redirect(url_for("asistencia.asistencia"))


@asistencia_bp.route("/asistencia", methods=["POST"])
@login_required
def enviar_qr_desde_asistencia():
    token = session.get("token")
    curso_id = _curso_actual()
    fecha_hoy = date.today().strftime("%Y-%m-%d")
    action = request.form.get("action")

    if action == "crear-clase":
        fecha_clase = request.form.get("fecha_clase")
        nombre_clase = request.form.get("nombre_clase")

        if not fecha_clase:
            flash("Debe seleccionar la fecha de la clase.", "error")
            return redirect(url_for("asistencia.asistencia"))
        if not nombre_clase:
            flash("Debe ingresar el nombre de la clase.", "error")
            return redirect(url_for("asistencia.asistencia"))

        status, data = post_json(
            "/asistencia/crear-clase",
            {
                "fecha_clase": fecha_clase,
                "nombre_clase": nombre_clase,
            },
            token=token,
        )

        if status == 200:
            flash("Clase creada exitosamente.", "success")
        else:
            flash(primer_mensaje_error(data, "No se pudo crear la clase."), "error")
        return redirect(url_for("asistencia.asistencia"))

    if action == "enviar_qr_hoy":
        status, data = post_json(
            "/asistencia/qr/enviar/todos",
            {
                "curso_id": curso_id,
                "fecha": fecha_hoy,
            },
            token=token,
        )

        if status == 200:
            flash(primer_mensaje_error(data, "QR enviados correctamente."), "success")
        else:
            flash(primer_mensaje_error(data, "No se pudieron enviar los QR."), "error")
        return redirect(url_for("asistencia.asistencia"))

    if action == "reprogramar-clase":
        return reprogramar_clase()

    flash("Accion de asistencia no reconocida.", "error")
    return redirect(url_for("asistencia.asistencia"))


@asistencia_bp.route("/asistencia/detalle/<int:id_alumno>", methods=["GET"])
@login_required
def detalle_asistencia_alumno(id_alumno):
    token = session.get("token")
    status, data = get_json(f"/asistencia/detalle/{id_alumno}", token=token)
    return jsonify(data), status
