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




app.run(debug=True)