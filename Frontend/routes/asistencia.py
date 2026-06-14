from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, flash
from services.api_client import get_json, post_json
from utils.auth import login_required

asistencia_bp = Blueprint("asistencia", __name__)


def primer_mensaje_error(data, fallback="Ocurrio un error."):
    errores = data.get("errors", []) if isinstance(data, dict) else []
    if errores:
        return errores[0].get("message", fallback)
    return data.get("mensaje", fallback) if isinstance(data, dict) else fallback


def cargar_alumnos_con_asistencia(token, curso_id, fecha):
    status, data = get_json("/asistencia/tabla", token=token)

    if status != 200 or not isinstance(data, dict):
        return status, [], primer_mensaje_error(data, "No se pudo cargar la asistencia.")

    alumnos = data.get("alumnos", [])

    for alumno in alumnos:
        alumno["id"] = alumno.get("padron")

        if alumno.get("estado") == "presente":
            alumno["estado_asistencia"] = "Presente"
        else:
            alumno["estado_asistencia"] = "Pendiente"

    return status, alumnos, None


def cargar_historial_asistencia(token, curso_id):
    status, data = get_json(f"/asistencia/historial?curso_id={curso_id}", token=token)
    if status in (401, 403):
        return status, [], "Sesion expirada."
    if status != 200 or not isinstance(data, dict):
        return status, [], primer_mensaje_error(data, "No se pudo cargar el historial de asistencia.")
    return status, data.get("historial", []), None


@asistencia_bp.route("/asistencia", methods=["GET"])
@login_required
def asistencia():
    token = session.get("token")
    curso_id = session.get("curso_id")

    fecha_hoy = date.today().strftime("%Y-%m-%d")

    if not token:
        session.clear()
        return redirect(url_for("auth.login"))

    if not curso_id:
        flash("No hay un curso seleccionado para gestionar la asistencia.", "error")
        return redirect(url_for("home.home"))

    status, data = get_json("/asistencia/tabla", token=token)

    if status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))

    alumnos = []

    if status == 200 and isinstance(data, dict):
        alumnos = data.get("alumnos", [])

        for alumno in alumnos:
            alumno["id"] = alumno.get("padron")

            if alumno.get("estado") == "presente":
                alumno["estado_asistencia"] = "Presente"
            else:
                alumno["estado_asistencia"] = "Pendiente"
    else:
        flash(primer_mensaje_error(data, "No se pudo cargar la asistencia."), "error")

    historial_status, historial, historial_error = cargar_historial_asistencia(token, curso_id)

    if historial_status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))

    if historial_error:
        flash(historial_error, "error")

    return render_template(
        "asistencia.html",
        alumnos=alumnos,
        fecha_hoy=fecha_hoy,
        historial=historial,
    )

@asistencia_bp.route("/asistencia", methods=["POST"])
@login_required
def enviar_qr_desde_asistencia():
    token = session.get("token")
    curso_id = session.get("curso_id")

    fecha_hoy = date.today().strftime("%Y-%m-%d")

    if not token:
        session.clear()
        return redirect(url_for("auth.login"))

    if not curso_id:
        flash("No hay un curso seleccionado para gestionar la asistencia.", "error")
        return redirect(url_for("home.home"))

    action = request.form.get("action", "individual")
    id_alumno = request.form.get("id_alumno")

    if action == "todos":
        status, data = post_json(
            "/asistencia/qr/enviar/todos",
            {
                "curso_id": curso_id,
                "fecha": fecha_hoy
            },
            token=token
        )

        if status in (401, 403):
            session.clear()
            return redirect(url_for("auth.login"))

        if status == 200:
            flash(primer_mensaje_error(data, "QR enviados correctamente."), "success")
        else:
            flash(primer_mensaje_error(data, "No se pudieron enviar los QR."), "error")

    else:
        if not id_alumno:
            flash("Debe seleccionar un alumno para enviar el QR.", "error")
        else:
            status, data = post_json(
                "/asistencia/qr/enviar",
                {
                    "id_alumno": id_alumno,
                    "fecha": fecha_hoy
                },
                token=token
            )

            if status in (401, 403):
                session.clear()
                return redirect(url_for("auth.login"))

            if status == 200:
                flash(primer_mensaje_error(data, "QR enviado correctamente."), "success")
            else:
                flash(primer_mensaje_error(data, "No se pudo enviar el QR."), "error")

    return redirect(url_for("asistencia.asistencia"))


@asistencia_bp.route("/asistencia-test", methods=["GET", "POST"])
def asistencia_test():
    fecha_hoy = date.today().strftime("%Y-%m-%d")

    if request.method == "POST":
        action = request.form.get("action")

        if action == "crear-clase":
            fecha_clase = request.form.get("fecha_clase")
            nombre_clase = request.form.get("nombre_clase")

            if not fecha_clase or not nombre_clase:
                flash("Debe completar la fecha y el nombre de la clase.", "error")
                return redirect(url_for("asistencia.asistencia_test"))

            status, data = post_json("/asistencia/crear-clase", {
                "fecha": fecha_clase,
                "nombre_clase": nombre_clase
            })

            if status in (200, 201):
                flash("Clase creada exitosamente.", "success")
            else:
                flash(primer_mensaje_error(data, "No se pudo crear la clase."), "error")

            return redirect(url_for("asistencia.asistencia_test"))

    # TABLA DE ALUMNOS
    status, data = get_json("/asistencia/tabla")

    alumnos = []

    if status == 200 and isinstance(data, dict):
        for alumno in data.get("alumnos", []):
            estado = alumno.get("estado", "pendiente")

            alumnos.append({
                "id": alumno.get("padron"),
                "nombre": alumno.get("nombre"),
                "apellido": alumno.get("apellido"),
                "email": alumno.get("email"),
                "estado_asistencia": "Presente" if estado == "presente" else "Pendiente"
            })

    # CLASES EXISTENTES
    status_clase, data_clases = get_json("/asistencia/clases")

    print("DEBUG STATUS CLASES:", status_clase)
    print("DEBUG DATA CLASES:", data_clases)

    clases = []

    if status_clase == 200:
        if isinstance(data_clases, list):
            clases = data_clases
        elif isinstance(data_clases, dict):
            clases = data_clases.get("clases", [])

    print("DEBUG CLASES FINAL:", clases)

    return render_template(
        "asistencia.html",
        alumnos=alumnos,
        fecha_hoy=fecha_hoy,
        historial=[],
        clases=clases,
    )


@asistencia_bp.route("/reprogramar-clase", methods=["POST"])
def reprogramar_clase():
    clase_key = request.form.get("clase_key")

    if not clase_key:
        flash("Seleccioná una clase para reprogramar", "error")
        return redirect(url_for("asistencia.asistencia_test"))

    fecha_actual, nombre_clase = clase_key.split("|||", 1)
    fecha_hoy = date.today().strftime("%Y-%m-%d")

    status, data = post_json("/asistencia/reprogramar-clase", {
        "fecha_actual": fecha_actual,
        "nombre_clase": nombre_clase,
        "nueva_fecha": fecha_hoy
    })

    if status in (200, 201):
        flash("Clase reprogramada correctamente para hoy.", "success")
    else:
        flash(primer_mensaje_error(data, "No se pudo reprogramar la clase."), "error")

    return redirect(url_for("asistencia.asistencia_test"))



