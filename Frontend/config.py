import os

# URL del backend Flask 
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:5000")

# Clave para firmar la sesión del navegador (cookie)
SECRET_KEY = os.environ.get("FRONTEND_SECRET_KEY", "clave-desarrollo-frontend")
