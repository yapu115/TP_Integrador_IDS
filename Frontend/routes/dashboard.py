from io import BytesIO

from flask import Blueprint, redirect, render_template, session, send_file, url_for
from utils.auth import login_required
from services.api_client import get_pdf

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    nombre = session.get("username", "Usuario")
    return render_template("dashboard.html", nombre=nombre)


def _proxy_pdf(endpoint, filename, params=None):
    curso_id = session.get("curso_id")
    if not curso_id:
        return redirect(url_for("cursos.seleccionar_curso"))

    token = session.get("token")
    extra = "&" + "&".join(f"{k}={v}" for k, v in params.items()) if params else ""
    status, data = get_pdf(f"/informes/{endpoint}?curso_id={curso_id}{extra}", token=token)

    if status == 200:
        return send_file(
            BytesIO(data),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )

    error_msg = "Error al generar el PDF."
    if isinstance(data, dict):
        errors = data.get("errors", [])
        if errors:
            error_msg = errors[0].get("message", error_msg)
    return f"<h2>Error {status}</h2><p>{error_msg}</p>", status


@dashboard_bp.route("/dashboard/informe_alumnos")
@login_required
def informe_alumnos():
    return _proxy_pdf("alumnos", "informe_alumnos.pdf", params={"abandono": "false"})

@dashboard_bp.route("/dashboard/informe_alumnos_todos")
@login_required
def informe_alumnos_todos():
    return _proxy_pdf("alumnos", "informe_alumnos_todos.pdf")


@dashboard_bp.route("/dashboard/informe_estadisticas")
@login_required
def informe_estadisticas():
    return _proxy_pdf("estadisticas", "informe_estadisticas.pdf")


@dashboard_bp.route("/dashboard/informe_equipos")
@login_required
def informe_equipos():
    return _proxy_pdf("equipos", "informe_equipos.pdf")
