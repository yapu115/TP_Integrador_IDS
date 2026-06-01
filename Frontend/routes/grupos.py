from flask import Blueprint, render_template, request
import requests

grupos_bp = Blueprint('grupos', __name__)

#Falta mover funciones a otro .py
def obtener_grupos()-> dict:
    #Falta la constante de la URL base de la API
    grupos = {}

    try:
        response = requests.get(f'{API_BASE_URL}/grupos')
        if response.status_code == 200:
            grupos = response.json()
        
    except Exception as e:
        #Falta pasar a libreria "logging"
        print("Error al obtener grupos.")
    return grupos

def obtener_alumnos_grupo(id_grupo)->dict:
    alumnos_grupo = {}
    try:
        response = requests.get(f'{API_BASE_URL}/grupos/{id_grupo}')
        if response.status_code == 200:
            alumnos_grupo = response.json()    
    except Exception as e:
        #Falta pasar a libreria "logging"
        print("Error al obtener los alumnos del grupo.")
    return 

@grupos_bp.route("/grupos", methods=["GET", "POST"])
def grupos():
    #Guardar grupos en un diccionario y pasarlos al template
    grupos = obtener_grupos()

    if request.method == "POST":
        #Se obtiene el id del grupo seleccionado para poder buscar sus alumnos
        id_grupo = request.form['boton-info-grupo']

        alumnos_grupo = obtener_alumnos_grupo(id_grupo)
        return render_template("grupos.html", grupos_dict=grupos, alumnos_grupo=alumnos_grupo)
    return render_template("grupos.html", grupos_dict=grupos)
