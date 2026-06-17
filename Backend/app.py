from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from curso.routes.asistencia import asistencia_bp
from curso.routes.evaluaciones import evaluacion_bp
from curso.routes.usuarios import usuarios_bp
from curso.routes.materiales import materiales_bp
from curso.routes.grupos import grupos_bp
from curso.routes.informes import informes_bp
from curso.routes.logs import logs_bp
from curso.routes.alumnos import alumnos_bp
from curso.routes.notas import notas_bp
from curso.routes.cursos import cursos_bp
from flask_cors import CORS

app = Flask(__name__, static_folder='curso/static')


CORS(app)


app.register_blueprint(cursos_bp)      
app.register_blueprint(asistencia_bp)
app.register_blueprint(evaluacion_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(materiales_bp)
app.register_blueprint(grupos_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(informes_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(notas_bp)       


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend funcionando"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
