import json
import urllib.error
import urllib.request

from config import BACKEND_URL


def get_pdf(path, token=None):
    """
    Llama al backend con GET y devuelve bytes PDF.
    """
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BACKEND_URL.rstrip('/')}{path}"
    request = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        raw = error.read()
        try:
            data = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError:
            data = {"errors": [{"message": raw.decode("utf-8", errors="replace") or "Error del servidor"}]}
        return error.code, data
    except urllib.error.URLError:
        return 0, {"errors": [{"message": "No se pudo conectar con el backend. ¿Está corriendo en el puerto 5000?"}]}


def get_json(path, token=None):
    """
    Llama al backend con GET y devuelve JSON desde el servidor Flask.
    """
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BACKEND_URL.rstrip('/')}{path}"
    request = urllib.request.Request(
        url,
        headers=headers,
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw) if raw else {}
            return response.status, data
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        return error.code, _json_error_response(raw)
    except urllib.error.URLError:
        return 0, _connection_error()


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
        return error.code, _json_error_response(raw)
    except urllib.error.URLError:
        return 0, _connection_error()


def put_json(path, body, token=None):
    """
    Llama al backend con PUT y JSON desde el servidor Flask.
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BACKEND_URL.rstrip('/')}{path}"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="PUT",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw) if raw else {}
            return response.status, data
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        return error.code, _json_error_response(raw)
    except urllib.error.URLError:
        return 0, _connection_error()


def patch_json(path, body, token=None):
    """
    Llama al backend con PATCH y JSON desde el servidor Flask.
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BACKEND_URL.rstrip('/')}{path}"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="PATCH",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw) if raw else {}
            return response.status, data
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        return error.code, _json_error_response(raw)
    except urllib.error.URLError:
        return 0, _connection_error()


def delete_json(path, token=None):
    """
    Llama al backend con DELETE desde el servidor Flask.
    """
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BACKEND_URL.rstrip('/')}{path}"
    request = urllib.request.Request(
        url,
        headers=headers,
        method="DELETE",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw) if raw else {}
            return response.status, data
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        return error.code, _json_error_response(raw)
    except urllib.error.URLError:
        return 0, _connection_error()


def post_multipart_file(path, field_name, file_storage, token=None):
    """
    Envia un archivo al backend con multipart/form-data.
    """
    boundary = "----tp-integrador-boundary"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    filename = file_storage.filename or "archivo.csv"
    file_bytes = file_storage.read()

    body = b"".join([
        f"--{boundary}\r\n".encode("utf-8"),
        (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode("utf-8"),
        b"Content-Type: text/csv\r\n\r\n",
        file_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode("utf-8"),
    ])

    url = f"{BACKEND_URL.rstrip('/')}{path}"
    request = urllib.request.Request(
        url,
        data=body,
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
        return error.code, _json_error_response(raw)
    except urllib.error.URLError:
        return 0, _connection_error()
