from requests import get, put, exceptions
from config import BACKEND_URL
url_api = f"{BACKEND_URL}/evaluaciones"
def actualizar_actividad(id_actividad, nombre, fecha, hora, descripcion,token=None):
    #actualiza una actividad en la base de datos
    try:
        url = f"{url_api}/{id_actividad}"
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        datos = {
            "nombre": nombre,
            "fecha": fecha,
            "hora": hora,
            "descripcion": descripcion
        }
        
        response = put(url, headers=headers,json=datos)

        return response.status_code in [200, 204]
    except exceptions.RequestException:
        return False

def obtener_actividad_por_id(id_actividad,token=None):
    try:
        url = f"{url_api}/{id_actividad}"
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = get(url,headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    except exceptions.RequestException:
        return None