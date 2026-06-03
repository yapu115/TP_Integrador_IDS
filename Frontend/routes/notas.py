from flask import Blueprint, render_template, request, session

from services.api_client import get_json, put_json
from utils.auth import login_required

notas_bp = Blueprint("notas", __name__)


def cargar_datos_notas(token, curso_id):
    status_alumnos, data_alumnos = get_json(f"/alumnos?curso_id={curso_id}&_limit=100", token=token)
    status_evaluaciones, data_evaluaciones = get_json("/evaluaciones", token=token)

    alumnos = data_alumnos.get("alumnos", []) if status_alumnos == 200 else []
    evaluaciones = data_evaluaciones if status_evaluaciones == 200 else []

    notas_por_alumno = {}
    for alumno in alumnos:
        status_notas, notas = get_json(f"/alumnos/{alumno['id']}/notas", token=token)
        if status_notas == 200:
            notas_por_alumno[alumno["id"]] = {
                nota["evaluacion"]: nota["nota"]
                for nota in notas
            }
        else:
            notas_por_alumno[alumno["id"]] = {}

    return status_alumnos, status_evaluaciones, alumnos, evaluaciones, notas_por_alumno


@notas_bp.route("/notas", methods=["GET"])
@login_required
def mostrar_notas():
    token = session.get("token")
    curso_id = session.get("curso_id")
    error = None

    status_alumnos, status_evaluaciones, alumnos, evaluaciones, notas_por_alumno = cargar_datos_notas(token, curso_id)

    if status_alumnos in (401, 403) or status_evaluaciones in (401, 403):
        session.clear()
        error = "La sesion expiro. Vuelva a iniciar sesion."
    elif status_alumnos not in (200, 204):
        error = "No se pudieron obtener los alumnos del curso."
    elif status_evaluaciones != 200:
        error = "No se pudieron obtener las evaluaciones."

    return render_template(
        "notas.html",
        alumnos=alumnos,
        evaluaciones=evaluaciones,
        notas_por_alumno=notas_por_alumno,
        error=error,
        exito=None,
    )


@notas_bp.route("/notas", methods=["POST"])
@login_required
def guardar_notas():
    token = session.get("token")
    errores = []
    guardadas = 0

    for campo, valor in request.form.items():
        if not campo.startswith("nota-") or valor == "":
            continue

        _, id_alumno, id_evaluacion = campo.split("-", 2)
        status, data = put_json("/notas", {
            "id_alumno": int(id_alumno),
            "id_evaluacion": int(id_evaluacion),
            "nota": float(valor),
        }, token=token)

        if status == 204:
            guardadas += 1
        else:
            mensaje = "No se pudo guardar una nota."
            if isinstance(data, dict):
                errores_backend = data.get("errors", [])
                if errores_backend:
                    mensaje = errores_backend[0].get("message", mensaje)
            errores.append(mensaje)

    status_alumnos, status_evaluaciones, alumnos, evaluaciones, notas_por_alumno = cargar_datos_notas(
        token,
        session.get("curso_id"),
    )

    error = errores[0] if errores else None
    if not error and status_alumnos not in (200, 204):
        error = "Las notas se guardaron, pero no se pudo recargar la lista de alumnos."
    if not error and status_evaluaciones != 200:
        error = "Las notas se guardaron, pero no se pudo recargar la lista de evaluaciones."

    return render_template(
        "notas.html",
        alumnos=alumnos,
        evaluaciones=evaluaciones,
        notas_por_alumno=notas_por_alumno,
        error=error,
        exito=f"Se guardaron {guardadas} notas correctamente." if guardadas and not error else None,
    )
