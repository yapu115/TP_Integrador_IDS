from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from services.api_client import get_json, post_json
from utils.auth import login_required

asistencia_bp = Blueprint("asistencia", __name__)


def primer_mensaje_error(data, fallback="Ocurrio un error."):
    errores = data.get("errors", []) if isinstance(data, dict) else []
    if errores:
        return errores[0].get("message", fallback)
    return data.get("mensaje", fallback) if isinstance(data, dict) else fallback


def cargar_alumnos_con_asistencia(token, curso_id, fecha):
    status, data = get_json(f"/alumnos?curso_id={curso_id}&_limit=100", token=token)
    if status in (401, 403):
        return status, [], "Sesion expirada."
    if status == 204:
        return status, [], None
    if status != 200 or not isinstance(data, dict):
        return status, [], primer_mensaje_error(data, "No se pudieron cargar los alumnos.")

    envios_status, envios_data = get_json(f"/asistencia/envios?curso_id={curso_id}&fecha={fecha}", token=token)
    envios_ids = set()
    if envios_status == 200 and isinstance(envios_data, dict):
        envios_ids = {
            envio.get("id_alumno")
            for envio in envios_data.get("envios", [])
        }

    alumnos = data.get("alumnos", [])
    for alumno in alumnos:
        alumno["estado_asistencia"] = "QR enviado" if alumno.get("id") in envios_ids else "Sin enviar"
        asist_status, asist_data = get_json(f"/alumnos/{alumno['id']}/asistencias", token=token)
        if asist_status == 200 and isinstance(asist_data, list):
            for registro in asist_data:
                if registro.get("fecha") == fecha and registro.get("presente"):
                    alumno["estado_asistencia"] = "Presente"
                    break

    return status, alumnos, None


def cargar_historial_asistencia(token, curso_id):
    status, data = get_json(f"/asistencia/historial?curso_id={curso_id}", token=token)
    if status in (401, 403):
        return status, [], "Sesion expirada."
    if status != 200 or not isinstance(data, dict):
        return status, [], primer_mensaje_error(data, "No se pudo cargar el historial de asistencia.")
    return status, data.get("historial", []), None


@asistencia_bp.route("/asistencia", methods=["GET", "POST"])
@login_required
def asistencia():
    token = session.get("token")
    curso_id = session.get("curso_id")
    fecha_hoy = date.today().strftime("%Y-%m-%d")
    fecha_seleccionada = request.form.get("fecha") or request.args.get("fecha") or fecha_hoy

    if request.method == "POST":
        accion = request.form.get("accion", "individual")
        id_alumno = request.form.get("id_alumno")
        if accion == "todos":
            status, data = post_json(
                "/asistencia/qr/enviar/todos",
                {
                    "curso_id": curso_id,
                    "fecha": fecha_seleccionada,
                },
                token=token,
            )
            if status in (401, 403):
                session.clear()
                return redirect(url_for("auth.login"))
            if status == 200:
                flash(primer_mensaje_error(data, "QR enviados correctamente."), "success")
            else:
                flash(primer_mensaje_error(data, "No se pudieron enviar los QR."), "error")
        elif not id_alumno:
            flash("Debe seleccionar un alumno para enviar el QR.", "error")
        else:
            status, data = post_json(
                "/asistencia/qr/enviar",
                {
                    "id_alumno": id_alumno,
                    "fecha": fecha_seleccionada,
                },
                token=token,
            )
            if status in (401, 403):
                session.clear()
                return redirect(url_for("auth.login"))
            if status == 200:
                flash(primer_mensaje_error(data, "QR enviado correctamente."), "success")
            else:
                flash(primer_mensaje_error(data, "No se pudo enviar el QR."), "error")

        return redirect(url_for("asistencia.asistencia", fecha=fecha_seleccionada))

    status, alumnos, error = cargar_alumnos_con_asistencia(token, curso_id, fecha_seleccionada)
    if status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))
    if error:
        flash(error, "error")

    historial_status, historial, historial_error = cargar_historial_asistencia(token, curso_id)
    if historial_status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))
    if historial_error:
        flash(historial_error, "error")

    return render_template(
        "asistencia.html",
        alumnos=alumnos,
        fecha_hoy=fecha_seleccionada,
        historial=historial,
    )
