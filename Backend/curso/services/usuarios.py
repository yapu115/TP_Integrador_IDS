from curso.db import get_connection
from werkzeug.security import check_password_hash, generate_password_hash
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


def obtener_usuario(id_usuario):
    """
    Función auxiliar para buscar un usuario por su ID y devolver sus datos sin la contraseña.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT id, username, email, rol, activo, ultimo_acceso, fecha_creacion
        FROM usuarios
        WHERE id = %s
    """
    cursor.execute(query, (id_usuario,))
    usuario = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if usuario:
        if usuario['ultimo_acceso']:
            usuario['ultimo_acceso'] = usuario['ultimo_acceso'].isoformat()
        if usuario['fecha_creacion']:
            usuario['fecha_creacion'] = usuario['fecha_creacion'].isoformat()
            
    return usuario


def crear_usuario(datos):
    """
    Comprueba duplicados, encripta la contraseña y guarda el usuario en la BD.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    retorno = None
    
    query_check = "SELECT id FROM usuarios WHERE username = %s OR email = %s"
    cursor.execute(query_check, (datos['username'], datos['email']))
    
    if cursor.fetchone():
        retorno = {"error": "RESOURCE_ALREADY_EXISTS", "mensaje": "El nombre de usuario o email ya están en uso."}
    else:
        password_hash = generate_password_hash(datos['password'])
        
        query = """
            INSERT INTO usuarios (username, email, password_hash, rol, activo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (datos['username'], datos['email'], password_hash, datos['rol'], datos['activo']))
        connection.commit()
        
        nuevo_id = cursor.lastrowid
        retorno = obtener_usuario(nuevo_id)
        
    cursor.close()
    connection.close()
    
    return retorno

def listar_usuarios(limit, offset):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    query_total = "SELECT COUNT(*) as total FROM usuarios"
    cursor.execute(query_total)

    total = cursor.fetchone()['total']
    
    query_data = """
        SELECT id, username, email, rol, activo, ultimo_acceso, fecha_creacion 
        FROM usuarios 
        LIMIT %s 
        OFFSET %s
    """
    cursor.execute(query_data, (limit, offset))
    usuarios = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    for u in usuarios:
        if u['ultimo_acceso']:
            u['ultimo_acceso'] = u['ultimo_acceso'].isoformat()
        if u['fecha_creacion']:
            u['fecha_creacion'] = u['fecha_creacion'].isoformat()
    
    return {"usuarios": usuarios, "total": total, "limit": limit, "offset": offset}


def actualizar_usuario(id_usuario, datos):
    usuario_actual = obtener_usuario(id_usuario)
    if not usuario_actual:
        return {"error": "NOT_FOUND", "mensaje": "Usuario no encontrado."}
    
    if not datos:
        return usuario_actual
        
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    retorno = None

    try:
        if "username" in datos or "email" in datos:
            check_username = datos.get("username", usuario_actual["username"])
            check_email = datos.get("email", usuario_actual["email"])
            
            query_check = "SELECT id FROM usuarios WHERE (username = %s OR email = %s) AND id != %s"
            cursor.execute(query_check, (check_username, check_email, id_usuario))
            
            if cursor.fetchone():
                return {"error": "RESOURCE_ALREADY_EXISTS", "mensaje": "El nombre de usuario o email ya están en uso."}
                
        campos_update = []
        valores_update = []
        
        if "username" in datos:
            campos_update.append("username = %s")
            valores_update.append(datos["username"])
            
        if "email" in datos:
            campos_update.append("email = %s")
            valores_update.append(datos["email"])
            
        if "password" in datos:
            campos_update.append("password_hash = %s")
            valores_update.append(generate_password_hash(datos["password"]))
            
        if "rol" in datos:
            campos_update.append("rol = %s")
            valores_update.append(datos["rol"])
            
        if "activo" in datos:
            campos_update.append("activo = %s")
            valores_update.append(datos["activo"])
            
        if campos_update:
            query = f"UPDATE usuarios SET {', '.join(campos_update)} WHERE id = %s"
            valores_update.append(id_usuario)
            
            cursor.execute(query, tuple(valores_update))
            connection.commit()
            
        retorno = obtener_usuario(id_usuario)
            
    finally:
        cursor.close()
        connection.close()
        
    return retorno