import sys
from pathlib import Path
from flask import Flask

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import SECRET_KEY
from routes.auth import auth_bp
from routes.home import home_bp
from routes.cursos import cursos_bp
from routes.evaluaciones import evaluaciones_bp
from routes.asistencia import asistencia_bp
from routes.grupos import grupos_bp
from routes.notas import notas_bp
from routes.alumnos import alumnos_bp
from routes.dashboard import dashboard_bp
from routes.materiales import materiales_bp
app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(evaluaciones_bp)
app.register_blueprint(asistencia_bp)
app.register_blueprint(grupos_bp)
app.register_blueprint(notas_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(materiales_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
