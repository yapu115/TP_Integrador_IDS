from config import BACKEND_URL
from flask import Blueprint, render_template, request, redirect, url_for,session
from requests import get, post, delete, exceptions
from services.evaluaciones import actualizar_actividad, obtener_actividad_por_id
from utils.auth import login_required
evaluaciones_bp = Blueprint('evaluaciones', __name__)
url_api = f"{BACKEND_URL}/evaluaciones"

@evaluaciones_bp.route("/evaluaciones",methods=["GET"])
@login_required
def mostrar_evaluaciones():
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        #Se guarda el json traido desde la api en la respuesta
        respuesta= get(url_api,headers=headers,timeout=5)
        #Si la respuesta es exitosa se transforma el json en un objeto de python mediante el metodo .json
        if respuesta.status_code==200:
            evaluaciones_data= respuesta.json()
        else:
            evaluaciones_data=[]
    except exceptions.RequestException:
        evaluaciones_data=[]
    return render_template('evaluaciones/evaluaciones.html',lista_evaluaciones=evaluaciones_data)

@evaluaciones_bp.route("/evaluaciones/crear", methods=["GET", "POST"])
@login_required
def crear_actividad():
    if request.method == "GET":
        return render_template("evaluaciones/crear_actividad.html")
    
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    #extrae y guarda los datos del formulario en un diccionario
    datos_formulario = {
        "nombre": request.form.get("nombre"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "descripcion": request.form.get("descripcion")
    }
    
    try:
        #envia el diccionario mediante la funcion post de request en formato json
        post(url_api, json=datos_formulario,headers=headers, timeout=5)
    except exceptions.RequestException as e:
        print(f"Error al conectar con la api: {e}")
        
    return redirect(url_for("evaluaciones.mostrar_evaluaciones"))


@evaluaciones_bp.route("/evaluaciones/eliminar/<int:id_actividad>", methods=["POST"])
@login_required
def eliminar_actividad(id_actividad):
    #Extrae el id de la actividad a eliminar y se la pasa a la api mediante la funcion delete
    url_eliminar = f"{url_api}/{id_actividad}"
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        respuesta = delete(url_eliminar,headers=headers,timeout=5)
        
        print(f"Status del borrado en la API: {respuesta.status_code}")
        
    except exceptions.RequestException as e:
        print(f"Error al conectar con la API para eliminar: {e}")
        
    return redirect(url_for("evaluaciones.mostrar_evaluaciones"))

@evaluaciones_bp.route('/evaluaciones/modificar/<int:id_actividad>', methods=['GET', 'POST'])
@login_required
def modificar_actividad(id_actividad):
    token = session.get("token")
    if request.method == 'GET':
        actividad_a_editar = obtener_actividad_por_id(id_actividad,token=token) 
        
        return render_template('evaluaciones/modificar_actividad.html', actividad=actividad_a_editar)

    if request.method == 'POST':
        nombre_nuevo = request.form.get('nombre')
        fecha_nueva = request.form.get('fecha')
        hora_nueva = request.form.get('hora')
        descripcion_nueva = request.form.get('descripcion')
        
        actualizar_actividad(id_actividad, nombre_nuevo, fecha_nueva, hora_nueva, descripcion_nueva,token=token)
        
        return redirect(url_for('evaluaciones.mostrar_evaluaciones'))