import os
import mysql.connector
import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "curso_universitario"),
        port=int(os.environ.get("DB_PORT", "3306"))
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
