from flask import Blueprint, render_template, request, redirect, url_for, session
from services.api_client import get_json, post_json, delete_json
from utils.auth import login_required

logs_bp = Blueprint('logs', __name__)

@logs_bp.route("/logs", methods=["GET"])
def mostrar_logs():
    token = session.get("token")
    status, logs_data = get_json("/log", token=token)
    if status == 200:
        lista_de_eventos = logs_data.get("logs", [])  
    else: 
       lista_de_eventos=[]

    return render_template('logs.html',lista_logs=lista_de_eventos)