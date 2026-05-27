import json
import urllib.error
import urllib.request

from config import BACKEND_URL


def post_json(path, body, token=None):
    """
    Llama al backend con POST y JSON desde el servidor Flask.
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BACKEND_URL.rstrip('/')}{path}"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw) if raw else {}
            return response.status, data
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        try:
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {"errors": [{"message": raw or "Error del servidor"}]}
        return error.code, data
    except urllib.error.URLError:
        return 0, {
            "errors": [{
                "message": "No se pudo conectar con el backend. ¿Está corriendo en el puerto 5000?",
            }]
        }
