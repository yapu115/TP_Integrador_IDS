from functools import wraps
from flask import session, redirect, url_for, request

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("token"):
            return redirect(url_for("auth.login", next=request.path))
        
        # Verificar que seleccionó un curso (salvo que esté intentando seleccionarlo, crearlo o cerrando sesión)
        if not session.get("curso_id") and request.endpoint not in ["cursos.seleccionar_curso", "cursos.crear_curso", "auth.logout"]:
            return redirect(url_for("cursos.seleccionar_curso"))
            
        return view(*args, **kwargs)
    return wrapped_view