from curso.db import get_connection

def alumno_existe(data):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    alumno_id = data.get("id_alumno")

    query = """
        SELECT id 
        FROM alumnos 
        WHERE id = %s
    """

    cursor.execute(query, (alumno_id,))
    alumno = cursor.fetchone()

    cursor.close()
    connection.close()

    return alumno is not None

def evaluacion_existe(data):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    evaluacion_id = data.get("id_evaluacion")

    query = """
        SELECT id 
        FROM tipos_evaluacion 
        WHERE id = %s
    """

    cursor.execute(query, (evaluacion_id,))
    evaluacion = cursor.fetchone()

    cursor.close()
    connection.close()

    return evaluacion is not None

def crear_nota(data):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    alumno_id = data.get("id_alumno")
    evaluacion_id = data.get("id_evaluacion")
    nota = data.get("nota")

    query_validar = """
        SELECT id 
        FROM notas 
        WHERE id_alumno = %s AND id_evaluacion = %s
    """

    cursor.execute(query_validar, (alumno_id, evaluacion_id))
    nota_existente = cursor.fetchone()

    if nota_existente:
        query_update = """
            UPDATE notas 
            SET nota = %s, fecha_carga = NOW() 
            WHERE id_alumno = %s AND id_evaluacion = %s
        """

        cursor.execute(query_update, (nota, alumno_id, evaluacion_id))

    else:
        query_crear = """
            INSERT INTO notas 
            (id_alumno, id_evaluacion, nota, fecha_carga) 
            VALUES (%s, %s, %s, NOW())
        """

        cursor.execute(query_crear, (alumno_id, evaluacion_id, nota))

    connection.commit()
    cursor.close()
    connection.close()


