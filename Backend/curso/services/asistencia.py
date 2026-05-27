import os
import smtplib
from email.message import EmailMessage

from curso.db import get_connection


# Genera un codigo QR simulado para pruebas del sistema.
# Actualmente no crea imagenes QR reales.
def generar_codigo_qr(id_alumno, fecha):
    retorno = f"ASISTENCIA-CLASE-{fecha}"
    if id_alumno:
        retorno = f"ASISTENCIA-{id_alumno}-{fecha}"
    return retorno


def alumno_existe(id_alumno):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT id FROM alumnos WHERE id = %s"
    cursor.execute(query, (id_alumno,))
    alumno = cursor.fetchone()

    cursor.close()
    connection.close()

    return alumno is not None


def obtener_alumno_contacto(id_alumno):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, nombre, apellido, email
        FROM alumnos
        WHERE id = %s
    """
    cursor.execute(query, (id_alumno,))
    alumno = cursor.fetchone()

    cursor.close()
    connection.close()

    return alumno


def enviar_mail_asistencia(destinatario, nombre_alumno, fecha, codigo_qr):
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_from = os.environ.get("SMTP_FROM", smtp_user)
    smtp_use_tls = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"

    if not smtp_host or not smtp_user or not smtp_password or not smtp_from:
        return {
            "error": "SMTP_NOT_CONFIGURED",
            "mensaje": (
                "Faltan variables de entorno SMTP_HOST, SMTP_USER, "
                "SMTP_PASSWORD y/o SMTP_FROM para enviar el correo."
            )
        }

    mensaje = EmailMessage()
    mensaje["Subject"] = f"Codigo QR de asistencia - {fecha}"
    mensaje["From"] = smtp_from
    mensaje["To"] = destinatario

    texto = (
        f"Hola {nombre_alumno},\n\n"
        "Este es tu codigo dinamico para registrar asistencia:\n\n"
        f"{codigo_qr}\n\n"
        "Escanealo o ingresalo en la plataforma para confirmar tu presencia.\n"
    )

    html = f"""
    <html>
      <body>
        <p>Hola {nombre_alumno},</p>
        <p>Este es tu codigo dinamico para registrar asistencia:</p>
        <p><strong>{codigo_qr}</strong></p>
        <p>Escanealo o ingresalo en la plataforma para confirmar tu presencia.</p>
      </body>
    </html>
    """

    mensaje.set_content(texto)
    mensaje.add_alternative(html, subtype="html")

    # Falta funcion para adjuntar o embeber la imagen QR real cuando este implementada.
    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
        if smtp_use_tls:
            smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(mensaje)

    return {"mensaje": "Email enviado exitosamente"}


def generar_qr_asistencia(fecha):
    codigo_qr = generar_codigo_qr(None, fecha)

    # Falta agregar el QR verdadero.
    qr_code_url = f"https://api.app.com/static/qrs/clase_{fecha.replace('-', '')}.png"

    return {
        "qr_code_url": qr_code_url,
        "codigo_qr": codigo_qr
    }


def enviar_qr_asistencia(id_alumno, fecha):
    retorno = None
    alumno = obtener_alumno_contacto(id_alumno)
    if not alumno:
        retorno = {"error": "NOT_FOUND", "mensaje": "No existe un alumno con ese id."}
    else:
        codigo_qr = generar_codigo_qr(id_alumno, fecha)
        nombre_alumno = f"{alumno['nombre']} {alumno['apellido']}"
        try:
            retorno = enviar_mail_asistencia(
                alumno["email"],
                nombre_alumno,
                fecha,
                codigo_qr
            )
            if "error" not in retorno:
                retorno["destinatario"] = alumno["email"]
                retorno["codigo_qr"] = codigo_qr
        except Exception as exc:
            retorno = {
                "error": "EMAIL_SEND_ERROR",
                "mensaje": f"No se pudo enviar el correo: {exc}"
            }
    return retorno


def registrar_asistencia(codigo_qr):
    retorno = None
    partes = codigo_qr.split("-")

    if len(partes) != 5 or partes[0] != "ASISTENCIA":
        retorno = {"error": "BAD_REQUEST", "mensaje": "El codigo QR es invalido o esta mal formado."}
    else:
        try:
            id_alumno = int(partes[1])
            fecha = f"{partes[2]}-{partes[3]}-{partes[4]}"

            if not alumno_existe(id_alumno):
                retorno = {"error": "NOT_FOUND", "mensaje": "El alumno asociado a este QR no existe en el sistema."}
            else:
                estado = "presente"

                connection = get_connection()
                cursor = connection.cursor(dictionary=True)

                query = """
                    INSERT INTO asistencias (id_alumno, fecha, estado, codigo_qr)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        estado = VALUES(estado),
                        codigo_qr = VALUES(codigo_qr)
                """

                cursor.execute(query, (id_alumno, fecha, estado, codigo_qr))
                connection.commit()

                cursor.close()
                connection.close()

                retorno = {"mensaje": "Asistencia registrada correctamente."}
        except ValueError:
            retorno = {"error": "BAD_REQUEST", "mensaje": "El codigo QR contiene datos corruptos."}

    return retorno


def obtener_asistencias_por_alumno(id_alumno):
    asistencias = None
    if alumno_existe(id_alumno):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT fecha, estado
            FROM asistencias
            WHERE id_alumno = %s
            ORDER BY fecha DESC
        """

        cursor.execute(query, (id_alumno,))
        asistencias_db = cursor.fetchall()

        cursor.close()
        connection.close()

        asistencias = []
        for a in asistencias_db:
            fecha_str = a["fecha"].strftime("%Y-%m-%d") if hasattr(a["fecha"], "strftime") else str(a["fecha"])
            asistencias.append({
                "fecha": fecha_str,
                "presente": a["estado"] == "presente"
            })

    return asistencias
