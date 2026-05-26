from flask import Blueprint, render_template, request, redirect, url_for, session

from services.api_client import post_json

auth_bp = Blueprint("auth", __name__)


def _primer_mensaje_error(data):
    errores = data.get("errors", [])
    if errores:
        return errores[0].get("message", "Ocurrió un error.")
    return data.get("mensaje", "Ocurrió un error.")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        status, data = post_json("/usuarios/login", {
            "username": username,
            "password": password,
        })

        if status == 200 and "token" in data:
            session["token"] = data["token"]
            session["username"] = username
            return redirect(url_for("home.index"))

        return render_template(
            "login.html",
            error=_primer_mensaje_error(data),
        )

    return render_template("login.html")


@auth_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirmar = request.form.get("confirmar_password", "")

        if password != confirmar:
            return render_template(
                "registrar.html",
                error="Las contraseñas no coinciden.",
            )

        if not nombre or not apellido:
            return render_template(
                "registrar.html",
                error="Nombre y apellido son obligatorios.",
            )

        username = email.split("@")[0] if "@" in email else email
        token = session.get("token")

        status, data = post_json("/usuarios", {
            "username": username,
            "email": email,
            "password": password,
            "rol": "profesor",
            "activo": True,
        }, token=token)

        if status == 201:
            return render_template(
                "registrar.html",
                exito="Usuario registrado correctamente. Ya puede iniciar sesión.",
            )

        if status in (401, 403) or not token:
            return render_template(
                "registrar.html",
                error="Para registrar usuarios debe iniciar sesión como administrador.",
            )

        return render_template(
            "registrar.html",
            error=_primer_mensaje_error(data),
        )

    return render_template("registrar.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
