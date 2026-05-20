from curso.db import get_connection


# Genera un código QR simulado para pruebas del sistema.
# Actualmente no crea imágenes QR reales.
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


def generar_qr_asistencia(fecha):
    codigo_qr = generar_codigo_qr(None, fecha)
    
    # Falta agregar el qr verdadero
    qr_code_url = f"https://api.app.com/static/qrs/clase_{fecha.replace('-', '')}.png"

    return {
        "qr_code_url": qr_code_url
    }


def enviar_qr_asistencia(id_alumno, fecha):
    retorno = None
    if not alumno_existe(id_alumno):
        retorno = {"error": "NOT_FOUND", "mensaje": "No existe un alumno con ese id."}
    else:
        codigo_qr = generar_codigo_qr(id_alumno, fecha)
        # Aquí iría la lógica para enviar el mail al alumno
        retorno = {"mensaje": "Email enviado exitosamente"}
    return retorno


def registrar_asistencia(codigo_qr):
    retorno = None
    partes = codigo_qr.split("-")
    
    if len(partes) != 5 or partes[0] != "ASISTENCIA":
        retorno = {"error": "BAD_REQUEST", "mensaje": "El código QR es inválido o está mal formado."}
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
            retorno = {"error": "BAD_REQUEST", "mensaje": "El código QR contiene datos corruptos."}

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