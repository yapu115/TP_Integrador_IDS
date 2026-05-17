from curso.db import get_connection
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timezone, timedelta
from curso.utils.security import SECRET_KEY

def login_usuario(username, password):
    """
    Se conecta a la base de datos para verificar las credenciales,
    y si son correctas, devuelve un Token JWT.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    retorno = {}
    
    query = "SELECT id, username, password_hash, rol, activo FROM usuarios WHERE username = %s"
    cursor.execute(query, (username,))
    usuario = cursor.fetchone()
    
    if not usuario or not check_password_hash(usuario['password_hash'], password):
        retorno = {"error": "UNAUTHORIZED", "mensaje": "Usuario o contraseña incorrectos."}
        
    elif not usuario['activo']:
        retorno = {"error": "UNAUTHORIZED", "mensaje": "La cuenta se encuentra inactiva."}
    
    else: 
        query_update = "UPDATE usuarios SET ultimo_acceso = NOW() WHERE id = %s"
        cursor.execute(query_update, (usuario['id'],))
        connection.commit()
        
        expiracion = datetime.now(timezone.utc) + timedelta(hours=24)
        token = jwt.encode({
            'id_usuario': usuario['id'],
            'username': usuario['username'],
            'rol': usuario['rol'],
            'exp': expiracion
        }, SECRET_KEY, algorithm="HS256")
        
        retorno = {"token": token}
        
    cursor.close()
    connection.close()
        
    return retorno
