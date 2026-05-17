from flask import Flask, jsonify
from curso.routes.asistencia import asistencia_bp

app = Flask(__name__)

app.register_blueprint(asistencia_bp)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend funcionando"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)