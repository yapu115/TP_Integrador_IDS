from flask import Flask, render_template, request

app = Flask(__name__)

#por mientras para probar el frontend

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario == "jeanca" and password == "1234":
            return "Inicio de sesión exitoso"

        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        # Procesar los datos del formulario de registro
        pass
    return render_template("registrar.html")


if __name__ == "__main__":
    app.run(debug=True)