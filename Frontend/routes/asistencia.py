from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, flash,jsonify 
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

    if status in (401, 403):
        return status, [], "Sesión expirada."

    if status != 200 or not isinstance(data, dict):
        return status, [], primer_mensaje_error(data, "No se pudo cargar la asistencia.")

    alumnos = []

    for alumno in data.get("alumnos", []):
        estado = alumno.get("estado", "pendiente")

        alumnos.append({
            "id": alumno.get("padron"),
            "padron": alumno.get("padron"),
            "nombre": alumno.get("nombre"),
            "apellido": alumno.get("apellido"),
            "email": alumno.get("email"),
            "estado_asistencia": "Presente" if estado == "presente" else "Pendiente"
        })

    return status, alumnos, None


def cargar_historial_asistencia(token, curso_id):
     return 200, [], None


@asistencia_bp.route("/asistencia", methods=["GET"])
@login_required
def asistencia():
    token = session.get("token")
    curso_id = session.get("curso_id") or 1
    session["curso_id"] = curso_id

    fecha_hoy = date.today().strftime("%Y-%m-%d")

    # TABLA DE ALUMNOS
    status, data = get_json("/asistencia/tabla", token=token)

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
                "condicion": alumno.get("condicion", "Sin definir")
            })
    else:
        flash(primer_mensaje_error(data, "No se pudo cargar la asistencia."), "error")

    # CLASES EXISTENTES
    status_clases, data_clases = get_json("/asistencia/clases", token=token)
    print("STATUS CLASES:", status_clases)
    print("DATA CLASES:", data_clases)

    clases = []

    if status_clases == 200:
        if isinstance(data_clases, list):
            clases = data_clases
        elif isinstance(data_clases, dict):
            clases = data_clases.get("clases", [])
    else:
        flash("No se pudieron cargar las clases obligatorias.", "error")

    clase_hoy = None

    for clase in clases:
        fecha_clase = str(clase.get('fecha'))[:10]

        if fecha_clase == fecha_hoy:
            clase_hoy = clase
            break

    hay_clase_hoy = clase_hoy is not None

    print("DEBUG ALUMNOS FRONT:", alumnos)


    return render_template(
        "asistencia.html",
        alumnos=alumnos,
        fecha_hoy=fecha_hoy,
        historial=[],
        clases=clases,
        hay_clase_hoy=hay_clase_hoy,
        clase_hoy=clase_hoy,
    )

@asistencia_bp.route("/reprogramar-clase", methods=["POST"])
@login_required
def reprogramar_clase():
    token = session.get("token")

    clase_seleccionada = request.form.get("clase_seleccionada")
    nueva_fecha = request.form.get("nueva_fecha")

    if not clase_seleccionada:
        flash("Seleccioná una clase para reprogramar.", "error")
        return redirect(url_for("asistencia.asistencia"))

    if not nueva_fecha:
        flash("Seleccioná la nueva fecha.", "error")
        return redirect(url_for("asistencia.asistencia"))

    partes = clase_seleccionada.split("|", 1)

    if len(partes) != 2:
        flash("La clase seleccionada no tiene un formato válido.", "error")
        return redirect(url_for("asistencia.asistencia"))

    fecha_actual = partes[0]
    nombre_clase = partes[1]

    status, data = post_json(
        "/asistencia/reprogramar-clase",
        {
            "fecha_actual": fecha_actual,
            "nombre_clase": nombre_clase,
            "nueva_fecha": nueva_fecha
        },
        token=token
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
    curso_id = session.get("curso_id") or 1
    session["curso_id"] = curso_id

    fecha_hoy = date.today().strftime("%Y-%m-%d")
    action = request.form.get("action")

    #Temporal
    print("ACTION RECIBIDA:", action)
    print("FORM RECIBIDO:", request.form)

    #crear clase
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
              "nombre_clase": nombre_clase
          },
          token=token
        )

       if status == 200:
           flash("Clase creada exitosamente.", "success")
       else:
           flash(primer_mensaje_error(data, "No se pudo crear la clase."), "error")

       return redirect(url_for("asistencia.asistencia"))

    #Reprogramar
    if action == "reprogramar-clase":
       clase_seleccionada = request.form.get("clase_seleccionada")
       nueva_fecha = request.form.get("nueva_fecha")

       if not clase_seleccionada:
          flash("Seleccioná una clase para reprogramar.", "error")
          return redirect(url_for("asistencia.asistencia"))

       if not nueva_fecha:
          flash("Seleccioná la nueva fecha.", "error")
          return redirect(url_for("asistencia.asistencia"))

    fecha_actual, nombre_clase = clase_seleccionada.split("|")

    status, data = post_json(
        "/asistencia/reprogramar-clase",
        {
            "fecha_actual": fecha_actual,
            "nombre_clase": nombre_clase,
            "nueva_fecha": nueva_fecha
        },
        token=token
    )

    if status == 200:
        flash("Clase reprogramada correctamente.", "success")
    else:
        flash(primer_mensaje_error(data, "No se pudo reprogramar la clase."), "error")

    return redirect(url_for("asistencia.asistencia"))

@asistencia_bp.route("/asistencia/detalle/<int:id_alumno>", methods=["GET"])
@login_required
def detalle_asistencia_alumno(id_alumno):
    token = session.get("token")

    status, data = get_json(
        f"/asistencia/detalle/{id_alumno}",
        token=token
    )

    return jsonify(data), status



@asistencia_bp.route("/asistencia/detalle/<int:id_alumno>", methods=["GET"])
@login_required
def detalle_asistencia_alumno(id_alumno):
    token = session.get("token")

    status, data = get_json(
        f"/asistencia/detalle/{id_alumno}",
        token=token
    )

    return jsonify(data), status

