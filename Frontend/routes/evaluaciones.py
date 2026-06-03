from flask import Blueprint, render_template, request, redirect, url_for, session
from services.api_client import get_json, post_json, delete_json
from services.evaluaciones import actualizar_actividad, obtener_actividad_por_id
from utils.auth import login_required

evaluaciones_bp = Blueprint('evaluaciones', __name__)

@evaluaciones_bp.route("/evaluaciones", methods=["GET"])
@login_required
def mostrar_evaluaciones():
    token = session.get("token")
    status, evaluaciones_data = get_json("/evaluaciones", token=token)
    
    if status != 200:
        evaluaciones_data = []

    return render_template('evaluaciones/evaluaciones.html', lista_evaluaciones=evaluaciones_data)

@evaluaciones_bp.route("/evaluaciones/crear", methods=["GET", "POST"])
@login_required
def crear_actividad():
    if request.method == "GET":
        return render_template("evaluaciones/crear_actividad.html")
    
    token = session.get("token")

    datos_formulario = {
        "nombre": request.form.get("nombre"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "descripcion": request.form.get("descripcion")
    }
    
    status, data = post_json("/evaluaciones", datos_formulario, token=token)
    if status not in (200, 201):
        print(f"Error al conectar con la api: {data}")
        
    return redirect(url_for("evaluaciones.mostrar_evaluaciones"))

@evaluaciones_bp.route("/evaluaciones/eliminar/<int:id_actividad>", methods=["POST"])
@login_required
def eliminar_actividad(id_actividad):
    token = session.get("token")
    
    status, data = delete_json(f"/evaluaciones/{id_actividad}", token=token)
    print(f"Status del borrado en la API: {status}")
        
    return redirect(url_for("evaluaciones.mostrar_evaluaciones"))

@evaluaciones_bp.route('/evaluaciones/modificar/<int:id_actividad>', methods=['GET', 'POST'])
@login_required
def modificar_actividad(id_actividad):
    token = session.get("token")
    if request.method == 'GET':
        actividad_a_editar = obtener_actividad_por_id(id_actividad, token=token) 
        
        return render_template('evaluaciones/modificar_actividad.html', actividad=actividad_a_editar)

    if request.method == 'POST':
        nombre_nuevo = request.form.get('nombre')
        fecha_nueva = request.form.get('fecha')
        hora_nueva = request.form.get('hora')
        descripcion_nueva = request.form.get('descripcion')
        
        actualizar_actividad(id_actividad, nombre_nuevo, fecha_nueva, hora_nueva, descripcion_nueva, token=token)
        
        return redirect(url_for('evaluaciones.mostrar_evaluaciones'))