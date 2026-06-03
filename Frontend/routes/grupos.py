from flask import Blueprint, render_template, request, session, jsonify
from utils.auth import login_required


grupos_bp = Blueprint('grupos', __name__)

#Falta mover funciones a otro .py
def obtener_grupos()-> list:
    API_BASE_URL = "http://localhost:5000"
    grupos = []

    try:
        response = requests.get(f'{API_BASE_URL}/grupos')
        if response.status_code == 200:
            grupos = response.json()
    except Exception as e:
        #Grupos.html muestra un mensaje de error si no se obtienen los grupos
        grupos=None
    return grupos

def obtener_alumnos_grupo(id_grupo)->dict:
    grupos = obtener_grupos()
    alumnos_grupo = None
    if grupos:
        for grupo in grupos:
            if grupo["id_grupo"] == id_grupo:
                alumnos_grupo = grupo["integrantes"]       
    return alumnos_grupo

    
@grupos_bp.route("/grupos", methods=["GET", "POST"])
@login_required
def grupos():
    #Guardar grupos en un diccionario y pasarlos al template
    grupos = obtener_grupos()

    if request.method == "POST":
        #Se obtiene el id del grupo seleccionado para poder buscar sus alumnos
        id_grupo = request.form['boton-info-grupo']

        alumnos_grupo = obtener_alumnos_grupo(id_grupo)
        if not alumnos_grupo:
            return render_template("grupos.html",grupos_dict=grupos,error="No se pudieron obtener los alumnos del grupo seleccionado.")
        return render_template("grupos.html", grupos_dict=grupos, alumnos_grupo=alumnos_grupo)
    return render_template("grupos.html", grupos_dict=grupos)