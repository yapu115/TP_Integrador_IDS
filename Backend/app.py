from flask import Flask, jsonify
from curso.routes.asistencia import asistencia_bp
from curso.routes.usuarios import usuarios_bp
from curso.routes.materiales import materiales_bp

app = Flask(__name__, static_folder='curso/static')

app.register_blueprint(asistencia_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(materiales_bp)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend funcionando"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)