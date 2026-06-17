import os
import smtplib
import qrcode

from curso.db import get_connection
from io import BytesIO
from email.message import EmailMessage
from datetime import date

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
        SELECT id, curso_id, nombre, apellido, email
        FROM alumnos
        WHERE id = %s
    """
    cursor.execute(query, (id_alumno,))
    alumno = cursor.fetchone()

    cursor.close()
    connection.close()

    return alumno


def obtener_alumnos_activos_curso(curso_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, nombre, apellido, email
        FROM alumnos
        WHERE curso_id = %s AND abandono = FALSE
        ORDER BY apellido, nombre
    """
    cursor.execute(query, (curso_id,))
    alumnos = cursor.fetchall()

    cursor.close()
    connection.close()

    return alumnos


def registrar_envio_qr(id_alumno, curso_id, fecha, codigo_qr, destinatario):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        INSERT INTO asistencia_qr_envios (id_alumno, curso_id, fecha, codigo_qr, destinatario)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            codigo_qr = VALUES(codigo_qr),
            destinatario = VALUES(destinatario),
            enviado_en = CURRENT_TIMESTAMP
    """
    cursor.execute(query, (id_alumno, curso_id, fecha, codigo_qr, destinatario))
    connection.commit()

    cursor.close()
    connection.close()


def obtener_envios_qr_curso(curso_id, fecha):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id_alumno, fecha, destinatario, enviado_en
        FROM asistencia_qr_envios
        WHERE curso_id = %s AND fecha = %s
    """
    cursor.execute(query, (curso_id, fecha))
    envios_db = cursor.fetchall()

    cursor.close()
    connection.close()

    envios = []
    for envio in envios_db:
        fecha_str = envio["fecha"].strftime("%Y-%m-%d") if hasattr(envio["fecha"], "strftime") else str(envio["fecha"])
        enviado_en = envio["enviado_en"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(envio["enviado_en"], "strftime") else str(envio["enviado_en"])
        envios.append({
            "id_alumno": envio["id_alumno"],
            "fecha": fecha_str,
            "destinatario": envio["destinatario"],
            "enviado_en": enviado_en
        })

    return envios


def obtener_historial_qr_curso(curso_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            e.fecha,
            COUNT(*) AS qr_enviados,
            SUM(CASE WHEN a.id_asistencia IS NULL THEN 0 ELSE 1 END) AS presentes
        FROM asistencia_qr_envios e
        LEFT JOIN asistencias a
            ON a.id_alumno = e.id_alumno
            AND a.fecha = e.fecha
            AND a.estado = 'presente'
        WHERE e.curso_id = %s
        GROUP BY e.fecha
        ORDER BY e.fecha DESC
    """
    cursor.execute(query, (curso_id,))
    historial_db = cursor.fetchall()

    cursor.close()
    connection.close()

    historial = []
    for item in historial_db:
        fecha_str = item["fecha"].strftime("%Y-%m-%d") if hasattr(item["fecha"], "strftime") else str(item["fecha"])
        historial.append({
            "fecha": fecha_str,
            "qr_enviados": int(item["qr_enviados"] or 0),
            "presentes": int(item["presentes"] or 0)
        })

    return historial


def enviar_mail_asistencia(destinatario, nombre_alumno, fecha, codigo_qr):
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_from = os.environ.get("SMTP_FROM", smtp_user)
    smtp_use_tls = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"

    if not smtp_host or not smtp_user or not smtp_password or not smtp_from:
        return{
            "error": "SMTP_NOT_CONFIGURED",
            "mensaje": (
                "Faltan variables de entorno SMTP_HOST, SMTP_USER,"
                "SMTP_PASSWORD o SMTP_FROM para enviar el correo"
            ) 
        }

    mensaje = EmailMessage()
    mensaje["Subject"] = f"Codigo QR de asistencia - {fecha}"
    mensaje["From"] = smtp_from
    mensaje["To"] = destinatario

    url_registro = f"http://127.0.0.1:5000/asistencia/registrar?codigo_qr={codigo_qr}"

    texto = (
        f"Hola {nombre_alumno}, \n\n"
        f"Este es tu código QR para registrar tu asistencia en el dia de hoy {fecha}. \n\n"
        f"Codigo: {codigo_qr}, \n\n"
        f"También podes ingresar desde este enlace:\n"
        f"{url_registro}\n\n"
        f"Escanealo o ingresa al enlace para confirmar tu presencia.\n"
    )

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding: 20px;" >
           <div style="max-width: 600px; margin: auto; background-color: white; padding: 25px; border-radius: 10px;"> 
               <h2 style="color: #263642; ">Registro de asistencia</h2>
               <p>Hola <strong>{nombre_alumno}</strong>,</p>
               <p>  
                  Este es tu codigo QR para registrar la asistencia correspondiente al dia <strong>{fecha}</strong>
               </p>

        <p style="text-align: center;">
           <img src="cid:qr_asistencia" alt="QR de asistencia" style="width: 220px; height: 220px;">
        </p>

        <p>
            <a href="{url_registro}">Registrar asistencia</a>
        </p>

        <p style="font-size: 13px; color: #666;">
           Código: {codigo_qr} 
        </p> 
       </div>
      </body>
    </html>
    """
 
    qr_bytes = generar_imagen_qr(url_registro)

    mensaje.set_content(texto)
    mensaje.add_alternative(html, subtype="html")

    mensaje_html = mensaje.get_payload()[1]
    mensaje_html.add_related(
        qr_bytes,
        maintype="image",
        subtype="png",
        cid="<qr_asistencia>"
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
        if smtp_use_tls:
            smtp.starttls()

        smtp.login(smtp_user, smtp_password)
        smtp.send_message(mensaje)

    return {"mensaje": "Se ha enviado correctamente el email"}


#Genera la imagen del qr, en memoria
def generar_imagen_qr(texto):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
        ) 

    qr.add_data(texto)
    qr.make(fit=True)
    
    imagen = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    imagen.save(buffer, format="PNG")

    return buffer.getvalue()

def generar_qr_asistencia(id_alumno, fecha):

    if not alumno_existe(id_alumno):
        return {
            "error": "NOT_FOUND", 
            "mensaje": "No existe un alumno con ese id."
            }

    codigo_qr = generar_codigo_qr(id_alumno, fecha)
    url_registro = f"http://127.0.0.1:5000/asistencia/registrar?codigo_qr={codigo_qr}" 

    return {
        "mensaje":"Se ha generado correctamente el QR",
        "id_alumno": id_alumno,
        "fecha": fecha,
        "codigo_qr": codigo_qr,
        "url_registrado": url_registro
    }

def enviar_qr_asistencia(id_alumno, fecha):
    
   #Busco al alumno, genera el qr y envia un mail con el qr
    alumno = obtener_alumno_contacto(id_alumno)
      
    if not alumno:
        return {
            "error": "NOT_FOUND",
            "mensaje":"No existe un alumno con ese id"
        }

    codigo_qr = generar_codigo_qr(id_alumno, fecha)
    nombre_alumno = f"{alumno['nombre']} {alumno['apellido']}"

        
    try:
        retorno = enviar_mail_asistencia(
            alumno["email"],
            nombre_alumno,
            fecha,
            codigo_qr
        )

        if retorno is None:
            return {
                "error": "EMAIL_SEND_ERROR",
                "mensaje": "La función enviar_mail_asistencia no devolvió ninguna respuesta."
            }

        if "error" in retorno:
            return retorno

        registrar_envio_qr(
            alumno["id"],
            alumno["curso_id"],
            fecha,
            codigo_qr,
            alumno["email"]
        )

        retorno["destinatario"] = alumno["email"]
        retorno["codigo_qr"] = codigo_qr

        return retorno

    except Exception as exc:
        return {
            "error": "EMAIL_SEND_ERROR",
            "mensaje": f"No se pudo enviar el correo: {exc}"
        }


def enviar_qr_asistencia_curso(curso_id, fecha):
    alumnos = obtener_alumnos_activos_curso(curso_id)

    if not alumnos:
        return {
            "error": "NOT_FOUND",
            "mensaje": "No hay alumnos activos en este curso."
        }

    enviados = []
    fallidos = []

    for alumno in alumnos:
        resultado = enviar_qr_asistencia(alumno["id"], fecha)
        if "error" in resultado:
            fallidos.append({
                "id_alumno": alumno["id"],
                "email": alumno["email"],
                "error": resultado.get("error"),
                "mensaje": resultado.get("mensaje")
            })
        else:
            enviados.append({
                "id_alumno": alumno["id"],
                "email": alumno["email"]
            })

    if not enviados:
        return {
            "error": "EMAIL_SEND_ERROR",
            "mensaje": "No se pudo enviar ningun correo a los alumnos activos.",
            "total_activos": len(alumnos),
            "fallidos": fallidos
        }

    return {
        "mensaje": f"Envio finalizado: {len(enviados)} enviados, {len(fallidos)} con error.",
        "total_activos": len(alumnos),
        "enviados": enviados,
        "fallidos": fallidos
    }

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

                retorno = {
                    "mensaje": "Asistencia registrada correctamente.",
                    "id_alumno": id_alumno,
                    "fecha": fecha
                }

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


def obtener_estado_asistencia_hoy():
    fecha = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query= """
    SELECT 
      alumnos.id,
      alumnos.legajo,
      alumnos.nombre, 
      alumnos.apellido,
      alumnos.email,
      COALESCE(asistencias.estado, 'pendiente') AS estado
    FROM alumnos
    LEFT JOIN asistencias
       ON alumnos.id = asistencias.id_alumno
       AND asistencias.fecha = %s
    ORDER BY alumnos.apellido, alumnos.nombre 
    """

    cursor.execute(query, (fecha,))
    alumnos = cursor.fetchall()

    cursor.close()
    connection.close()

    return{
        "fecha": fecha,
        "alumnos": alumnos
    }

def crear_clase_obligatoria(fecha, nombre_clase):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            INSERT INTO clases_obligatorias (fecha, nombre_clase)
            VALUES (%s, %s)
        """, (fecha, nombre_clase))

        connection.commit()

        return {
            "mensaje": "Clase creada exitosamente."
        }

    except Exception as e:
        print("ERROR crear_clase_obligatoria:", e)
        return {
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def obtener_clases_obligatorias():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id_clase AS id, 
            DATE_FORMAT(fecha, '%Y-%m-%d') AS fecha,
            nombre_clase
            FROM clases_obligatorias
            ORDER BY fecha DESC, id_clase DESC
            """
        
        cursor.execute(query)
        clases = cursor.fetchall()

        return clases

    except Exception as e:
        print("ERROR obtener_clases_obligatorias:", e)
        return {
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def reprogramar_clase_obligatoria(fecha_actual, nombre_clase, nueva_fecha):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE clases_obligatorias
            SET fecha = %s
            WHERE fecha = %s
            AND nombre_clase = %s
        """, (nueva_fecha, fecha_actual, nombre_clase))

        connection.commit()

        if cursor.rowcount == 0:
            return {
                "error": "NOT_FOUND",
                "mensaje": "No se encontró la clase para reprogramar."
            }

        return {
            "mensaje": "Clase reprogramada correctamente."
        }

    except Exception as e:
        print("ERROR reprogramar_clase_obligatoria:", e)
        return {
            "error": str(e),
            "mensaje": "No se pudo reprogramar la clase."
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def obtener_detalle_clases_alumno(id_alumno):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                DATE_FORMAT(c.fecha, '%Y-%m-%d') AS fecha,
                c.nombre_clase,
                COALESCE(a.estado, 'pendiente') AS estado
            FROM clases_obligatorias c
            LEFT JOIN asistencias a
                ON a.id_alumno = %s
                AND a.fecha = c.fecha
            ORDER BY c.fecha DESC, c.id_clase DESC
        """

        cursor.execute(query, (id_alumno,))
        clases = cursor.fetchall()

        return {
            "id_alumno": id_alumno,
            "clases": clases
        }

    except Exception as e:
        print("ERROR obtener_detalle_clases_alumno:", e)
        return {
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def obtener_detalle_clases_alumno(id_alumno):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                DATE_FORMAT(c.fecha, '%Y-%m-%d') AS fecha,
                c.nombre_clase,
                COALESCE(a.estado, 'pendiente') AS estado
            FROM clases_obligatorias c
            LEFT JOIN asistencias a
                ON a.id_alumno = %s
                AND a.fecha = c.fecha
            ORDER BY c.fecha DESC, c.id_clase DESC
        """

        cursor.execute(query, (id_alumno,))
        clases = cursor.fetchall()

        return {
            "id_alumno": id_alumno,
            "clases": clases
        }

    except Exception as e:
        print("ERROR obtener_detalle_clases_alumno:", e)
        return {
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()