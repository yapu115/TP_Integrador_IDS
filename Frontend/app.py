from flask import Flask, render_template, request, redirect

app = Flask(__name__)

#por mientras para probar el frontend

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario == "jeanca" and password == "1234":
            return redirect("/dashboard")

        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", nombre="Jeanca")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/grupos")
def grupos():
    return render_template("grupos.html")

@app.route("/asistencia")
def asistencia():
    return render_template("asistencia.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        # Procesar los datos del formulario de registro
        pass
    return render_template("registrar.html")


if __name__ == "__main__":
    app.run(debug=True)