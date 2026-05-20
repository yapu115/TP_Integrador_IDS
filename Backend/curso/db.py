import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="test",
        database="curso_universitario"
    )

def execute(query):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    finally:
        cursor.close()
        connection.close
    return results

