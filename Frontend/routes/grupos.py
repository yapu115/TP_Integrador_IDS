from flask import Blueprint, render_template, request, session, redirect, url_for
from services.api_client import get_json, post_json, delete_json
from utils.auth import login_required

grupos_bp = Blueprint('grupos', __name__)

def _cargar_grupos(token, curso_id):
    status, data = get_json(f"/grupos?curso_id={curso_id}", token=token)
    if status == 200 and isinstance(data, list):
        return data
    return []

@grupos_bp.route("/grupos", methods=["GET", "POST"])
@login_required
def grupos():
    token = session.get("token")
    curso_id = session.get("curso_id")

    id_grupo_seleccionado = None
    if request.method == "POST":
        id_grupo_seleccionado = request.form.get("boton-info-grupo")

    lista_grupos = _cargar_grupos(token, curso_id)

    integrantes = None
    nombre_grupo_seleccionado = None
    if id_grupo_seleccionado:
        accion_boton = request.form.get("action") 
        if accion_boton == "Ver integrantes del grupo":
            status, detalle = get_json(f"/grupos/{id_grupo_seleccionado}", token=token)
            if status == 200:
                nombre_grupo_seleccionado = detalle.get("nombre")
                ids_integrantes = detalle.get("integrantes", [])

                integrantes = []
                for id_alumno in ids_integrantes:
                    st, alumno = get_json(f"/alumnos/{id_alumno}", token=token)
                    if st == 200:
                        integrantes.append(alumno)
        elif accion_boton == "ELIMINAR GRUPO":
            status, detalle = delete_json(f"/grupos/{id_grupo_seleccionado}", token=token)
            if status == 204:
                print(f"Status del borrado en la API: {status}")
                return redirect(url_for("grupos.grupos"))
    # Cargar alumnos y evaluaciones para el formulario de crear/editar grupo
    st_al, data_al = get_json(f"/alumnos?curso_id={curso_id}&_limit=100", token=token)
    lista_alumnos = data_al.get("alumnos", []) if st_al == 200 else []

    st_ev, data_ev = get_json("/evaluaciones", token=token)
    lista_evaluaciones = data_ev if st_ev == 200 else []

    return render_template(
        "grupos.html",
        grupos=lista_grupos,
        integrantes=integrantes,
        nombre_grupo_seleccionado=nombre_grupo_seleccionado,
        alumnos_curso=lista_alumnos,
        evaluaciones_curso=lista_evaluaciones
    )

@grupos_bp.route("/grupos/crear", methods=["POST"])
@login_required
def crear_grupo():
    token = session.get("token")
    curso_id = session.get("curso_id")
    nombre = request.form.get("nombre")
    integrantes = request.form.getlist("integrantes")
    evaluaciones = request.form.getlist("evaluaciones")
    
    integrantes = [int(i) for i in integrantes if i.isdigit()]
    evaluaciones = [int(e) for e in evaluaciones if e.isdigit()]

    if nombre:
        post_json(f"/grupos?curso_id={curso_id}", {
            "nombre": nombre,
            "integrantes": integrantes,
            "ids_tp": evaluaciones
        }, token=token)

    return redirect(url_for("grupos.grupos"))