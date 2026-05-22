import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="curso_universitario"
    )

def execute(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if query.lstrip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
            connection.commit()
            return cursor.rowcount

        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
