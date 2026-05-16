AUTH
POST /auth/login
POST /auth/logout
POST /auth/register

ALUMNOS
GET /alumnos
POST /alumnos
GET /alumnos/<id>
PATCH /alumnos/<id>
DELETE /alumnos/<id>
POST /alumnos/importar-csv

EVALUACIONES
GET /tipos-evaluacion
POST /tipos-evaluacion
PATCH /tipos-evaluacion/<id>
DELETE /tipos-evaluacion/<id>

NOTAS
POST /notas
GET /notas/alumno/<id_alumno>
GET /notas/evaluacion/<id_evaluacion>

GRUPOS
GET /grupos
POST /grupos
POST /grupos/<id>/alumnos

ASISTENCIA
POST /asistencia/generar-qr
POST /asistencia/registrar
GET /asistencia

INFORMES
GET /informes/alumnos.pdf
GET /informes/equipos.pdf
GET /informes/estadisticas-aprobacion.pdf