# Plataforma de Administración de Cursos Universitarios

Sistema web integral para gestionar en forma completa el ciclo de vida de un curso universitario, abarcando alumnos, evaluaciones, grupos, asistencia, notas y auditoría.

## Integrantes (nombre-legajo)
- Franco Yapura / 115280
- Jean Carlos / 114122
- Federico Andrada de Palomera / 115549
- Franco Miniaci/114868
- Felipe Ricardo Cravero / 114507
- Zlatna Vallejos / 114909
- Julian Fernandez / 114563

## Características Principales

* **Seguridad y Auditoría:**
  * Autenticación de usuarios mediante tokens (JWT/Bearer).
  * Manejo de usuarios (Administradores/Profesores) y registro de actividad (log) del sistema.
* **Gestión de Alumnos:**
  * ABM completo de alumnos e importación masiva mediante archivos CSV.
  * Control de estado de los alumnos (seguimiento de abandono de la materia).
* **Evaluaciones y Notas:**
  * ABM de tipos de evaluación (Parciales, Parcialitos, Trabajos Prácticos, etc.).
  * Sistema de carga y registro de calificaciones.
* **Gestión de Equipos (Grupos):**
  * ABM de equipos integrados por "n" alumnos y asociación dinámica a uno o varios Trabajos Prácticos.
* **Asistencia Inteligente:**
  * Sistema de asistencia mediante generación de códigos QR dinámicos (con referencia al alumno y fecha).
  * Envío automatizado del código QR por correo electrónico.
* **Dashboard e Informes (PDF):**
  * Listado de alumnos con filtros dinámicos y estadísticas generales de aprobación.
  * Generación de reportes en PDF utilizando ReportLab.
* **Características Adicionales:**
  * Sección para carga de material de estudio (visualización pública y gestión protegida).

---
## Arquitectura

```
Flujo de una request:

   Frontend (Web App en Flask,puerto 5001)
        |
   Templates/ (El usuario ve e interactúa con el HTML/CSS)
        |
   Services/api_client.py (Arma la petición HTTP con el JWT)
        |
   Petición HTTP (JSON / Bearer Token)
        |
        v
   Flask API (Backend, puerto 5000)
        |
   Curso/routes/ (Recibe el endpoint, ej: /alumnos o /notas)
        |
   Curso/validators/ (Valida los datos de entrada)
        |
   Curso/services/ (Ejecuta la lógica)
        |
        |  
        v
   MySQL Database (Servidor local, puerto 3306)

```


##  Estructura del Proyecto
```
Backend/
├── app.py                      # Punto de entrada de la API Flask (Puerto 5000)
├── init.sh                     # Script Bash automatizado para setup del entorno
├── requirements.txt            # Archivo de dependencias del proyecto Python
├── .env.example                # Plantilla de referencia para configuración externa
├── data/                       # Recursos y scripts de persistencia de datos
│   ├── Diagrama BD.png         # Modelo de entidad-relación de la base de datos
│   ├── init_db.sql             # Estructura de tablas e inicialización de MySQL
│   ├── migration_asistencia_qr_envios.sql
│   └── seed_data.sql           # Datos de prueba para poblar el sistema
├── docs/                       # Documentación técnica de la API (Swagger/OpenAPI)
└── curso/                      # Paquete principal de la aplicación (Módulos de negocio)
├── db.py                       # Configuracion de acceso a la base de datos y funciones para ejecutar querys
├── init.py                     # Inicializador del módulo
├── routes/                     # Endpoints REST de todo el proyecto
│   ├── alumnos.py
│   ├── asistencia.py
│   ├── cursos.py
│   ├── evaluaciones.py
│   ├── grupos.py
│   ├── informes.py
│   ├── logs.py
│   ├── materiales.py
│   ├── notas.py
│   └── usuarios.py
├── services/               # Capa de Lógica de Negocio (Procesamiento pesado)
│   ├── alumnos.py
│   ├── asistencia.py       
│   ├── cursos.py
│   ├── evaluaciones.py
│   ├── grupos.py
│   ├── informes.py        
│   ├── logs.py
│   ├── materiales.py
│   ├── notas.py
│   └── usuarios.py
├── static/materiales/      # Almacenamiento local de archivos estáticos cargados
│   └── Proyecto_Final_IDS_2026C1.pdf
├── utils/                  # Funciones utiles y auxiliares  del sistema
│   ├── security.py         
│   └── utils.py
└── validators/             # Capa de Validaciones de los endpoints
│   ├── alumnos.py
│   ├── asistencia.py       
│   ├── cursos.py
│   ├── evaluaciones.py
│   ├── grupos.py
│   ├── informes.py        
│   ├── logs.py
│   ├── materiales.py
│   ├── notas.py
│   └── usuarios.py

```

```
Frontend/
├── app.py                      # Punto de entrada de la aplicación Frontend Flask
├── config.py                   # Configuraciones generales del cliente web
├── init.sh                     # Script para inicialización del entorno virtual de Python
├── requirements.txt            # Dependencias de Python para el Frontend
├── package.json                # 
├── vite.config.js              # 
├── eslint.config.js            # 
├── index.html                  # Punto de entrada HTML base para Vite
├── .gitignore                  # Archivo para ignorar archivos en el repositorio Git
├── public/                     # Recursos públicos estáticos globales
│   ├── favicon.svg             # Icono de la pestaña del navegador
│   └── icons.svg               # 
├── routes/                     # Controladores de Flask que gestionan y renderizan las páginas
│   ├── alumnos.py
│   ├── asistencia.py
│   ├── auth.py                 # (Gestión de sesiones y login de usuarios)
│   ├── cursos.py
│   ├── dashboard.py            # (Métricas generales y estadísticas del panel)
│   ├── evaluaciones.py
│   ├── grupos.py
│   ├── home.py                 # (Página de inicio y accesos públicos)
│   ├── materiales.py
│   └── notas.py
├── services/                   # Capa para el consumo de la API del Backend
│   ├── api_client.py           # Cliente HTTP configurado para conectarse con el Backend
│   └── evaluaciones.py
├── static/css/                 # Archivos de estilo independientes para cada interfaz
│   ├── alumnos.css
│   ├── asistencia.css
│   ├── auth.css
│   ├── base.css                
│   ├── crear_cursos.css
│   ├── cursos.css
│   ├── dashboard.css
│   ├── evaluaciones.css
│   ├── grupos.css
│   ├── home.css
│   ├── materiales.css
│   └── notas.css
├── src/                        # 
│   ├── assets/                 # 
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── templates/                  # Vistas HTML renderizadas dinámicamente por Flask (Jinja2)
│   ├── evaluaciones/           # Plantillas específicas del módulo de evaluaciones
│   ├── alumnos.html
│   ├── asistencia.html
│   ├── base.html               
│   ├── crear_curso.html
│   ├── cursos.html
│   ├── dashboard.html
│   ├── grupos.html
│   ├── home.html
│   ├── login.html
│   ├── materiales.html
│   ├── notas.html
│   └── registrar.html
└── utils/                      # Funciones auxiliares para el Frontend
```

## Tecnologías Utilizadas

| Componente | Tecnología / Librería | Descripción |
| :--- | :--- | :--- |
| **Backend** | Python 3 / Flask (v3.0.3) | Framework Web Base y lógica de negocio |
| **Base de Datos** | MySQL / `mysql-connector-python` | Almacenamiento relacional de datos |
| **Frontend** | HTML5, CSS3, JavaScript | Interfaz de usuario |
| **Seguridad** | PyJWT (v2.8.0) & Werkzeug | Gestión de tokens de seguridad y hashing de contraseñas |
| **Herramientas** | qrcode, pillow, reportlab | Generación de QR, procesamiento de imágenes y reportes PDF |
| **Documentación**| Swagger | Especificación de la API (`Backend/docs/swagger.yaml`) |

## Logica de algunas caracteristicas

### 1. El Flujo de Inicio de Sesión (Login)
El usuario ingresa sus credenciales en la vista de templates/login.html.

El controlador de Frontend (routes/auth.py) recibe los datos y, mediante el api_client.py, hace un POST /usuarios/login hacia el Backend.

El Backend valida las credenciales contra la base de datos (para verificar el hash de la contraseña). Si son correctas, genera un JWT firmado con una clave secreta y un tiempo de expiración.

El Backend responde al Frontend con el token JSON. El Frontend almacena este token en la sesión de Flask (session['token']) para mantener al usuario logueado en el navegador de forma segura.
```
Frontend (Cliente)                                          Backend (API REST)
     │                                                          │
     │─── GET /alumnos ────────────────────────────────────────>│
     │    Header: Authorization: Bearer <JWT_TOKEN>             │
     │                                                          │
     │                                                  [utils/security.py]
     │                                                  • Decodifica el token
     │                                                  • Verifica firma y expiración
     │                                                  • Extrae rol (Admin/Profesor)
     │                                                          │
     │<── 200 OK (JSON Data) ───────────────────────────────────│
```
### 2. Sistema de asistencia
El sistema de asistencia posee un formato que lo hace eficiente y seguro, cuenta con caracteristicas como las siguientes:

1. Optimización de Memoria (Códigos QR)
Los códigos QR se generan dinámicamente en la memoria RAM en formato PNG. Esto evita el desgaste del almacenamiento físico del servidor.
La URL del QR codifica los datos del alumno bajo el formato ASISTENCIA-{id_alumno}-{fecha}.

2. Envío Masivo por Correo (SMTP)
Al momento de enviarse los correos se seleccionan solo los alumnos activos (abandono = FALSE).
Se utiliza la librería smtplib con cifrado TLS, permitiendo que los datos viajen de forma segura.
Los QR se incrustan en el cuerpo del correo (HTML/Texto plano), suprimiendo su logica y evitando que el usuario tenga que descargar archivos adjuntos.

3. Robustez y Seguridad
Soporta peticiones POST y enlaces GET optimizados para móviles.
Para evitar errores por doble escaneo o reenvíos, se usa la cláusula SQL ON DUPLICATE KEY UPDATE. Si el registro ya existe, se actualizan los metadatos de auditoría en lugar de duplicar la asistencia.

4. Gestión del Calendario
Flexibilidad: Permite reprogramar clases obligatorias y alterar el calendario escolar.

```
Dispositivo Móvil (Escaneo)                               Backend (API REST)
     │                                                          │
     │─── GET /asistencia/registrar?codigo_qr=... ─────────────>│
     │    Query: ASISTENCIA-12-2026-06-09                       │
     │                                                          │
     │                                               [services/asistencia.py]
     │                                               • Descompone el string con .split("-")
     │                                               • Extrae id_alumno (12) y fecha
     │                                                          │
     │                                                          │
     │                                                          │
     │<── 200 OK (HTML Éxito) / 400 (Error) ────────────────────│
```

### 3. Sistema de logs (Registro de actividad)
El sistema de logs permite registrar cualquier actividad interactiva de la web, su funcionamiento esta dado por las siguientes caracteristicas:

1. Automatización.
Se utiliza un decorador parametrizado (@registrar_actividad("Nombre de la Acción")) que envuelve las rutas de la aplicación. Este intercepta la petición, espera la ejecución de la función original y evalúa el código de estado HTTP devuelto de forma dinámica.

2.Reutilización.
Aprovecha el ciclo de vida global del objeto request. El sistema lee los datos del usuario (usuario_actual). Estos datos son inyectados previamente en la petición por el decorador de autenticación (@token_required), asegurando una identificación precisa sin necesidad de realizar nuevas consultas a la base de datos.

```
Frontend (Cliente)                                        Backend (API REST)
     │                                                          │
     │─── POST /usuarios (Crear Usuario) ─────────────────────> │
     │    Header: Authorization: Bearer                         │
     │    Body: {"nombre": "Juan", "rol": "admin"}              │
     │                                                          │
     │                                                    [utils/security]
     │                                                 @token_required valida e inyecta `usuario_actual`
     │                                                 @registrar_actividad envuelve la función
     │                                                          │
     │                                                    [route/usuario]
     │                                                 Ejecuta la lógica principal (Crear usuario)
     │                                                 Devuelve la tupla de respuesta y estado (201)
     │                                                          │
     │                                                    [utils/utils]
     │                                                 @registrar_actividad evalúa la respuesta (201)
     │                                                 Extrae el Body y el Usuario de `request`
     │                                                          │
     │                                                      [services/logs.py]
     │                                                          │
     │                                                      Crear_log(datos para la creacion del log)
     │                                                          │
     │<── 201 Created (JSON Data) ──────────────────────────────│
```
### 4. Dashbord (listado de alumnos)
Se cuenta con un sistema para manejar grandes volúmenes de datos de alumnos de forma eficiente. El mismo posee:

1. Filtrado Dinámico de Estudiantes, filtra según la condición académica usando el campo booleano abandono mediante cláusulas AND dinámicas en SQL.
   Cuando el usuario escribe un nombre o legajo, el sistema busca en tiempo real y por coincidencias parciales de forma instantánea y fluida.

2. Ingesta y Exportación Masiva (Archivos CSV)
Importación (POST): El Frontend envía un archivo vía Multipart/Form-Data. El Backend lo procesa en UTF-8 usando un buffer de memoria (io.StringIO) y la librería csv.DictReader, transformando las filas en tuplas para una inserción rápida en la base de datos.

Exportación (GET): Genera la descarga de la lista filtrada en tiempo real. Utiliza la clase Response de Flask con el tipo text/csv y la cabecera Content-Disposition: attachment. El navegador descarga un archivo físico (alumnos_curso_{id}.csv) generado directamente desde la memoria RAM.

### 5. Gestion de grupos
El sistema permite armar grupos de alumnos, asignarles evaluaciones y mostrar sus datos.Algunas de sus caracteristicas son:

1.Limpiar los datos duplicados que genera la base de datos.
Cuando se cruzan tablas en la base de datos (como Grupos, Evaluaciones e Integrantes), los motores SQL suelen duplicar filas.
para ello la función _agrupar_resultados() toma ese "bloque" de datos desordenado y usa conjuntos mutables (set()) en la memoria del servidor para unificar los IDs repetidos.

2.Integridad de los datos.
Crear o modificar un grupo exige tocar varias tablas al mismo tiempo. Para evitar que un grupo se cree sin alumnos o con datos incompletos
los cambios se guardan físicamente en el disco de la base de datos solo si todas las inserciones terminan con éxito.

Arrepentimiento (Rollback): Si algo falla en el medio el sistema ejecuta un rollback. Esto borra cualquier cambio parcial que se haya hecho en esa operación.

3. Carga eficiente en la Pantalla.
Los nombres y detalles de los integrantes no se descargan hasta que el usuario hace clic específicamente en el botón de información de un equipo.
Esto evita que la página web no se vuelva lenta al listar decenas de grupos


## Requisitos previos

- Python 3.10+
- Una instalacion local de MySQL 8
- Linux Ubuntu (Tambien sirve para Mac o en windows habiendo descargado WSL)

#### Instalacion de la base de datos

Si ya tenes MySQL 8 corriendo en tu maquina (puerto `3306` por default):

1. Con los comandos de abajo se crean las tablas y datos de prueba.

   ```bash
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS curso_universitario;"
   mysql -u root -p curso_universitario < data/init_db.sql
   mysql -u root -p curso_universitario < data/seed_data.sql
   ```
   
2. Verificar que las tablas se hayan creado:

   ```bash
   mysql -u root -p -e "USE curso_universitario; SHOW TABLES;"
   ```
   Deberia aparecer por pantalla usuarios,alumnos,tipos_evaluacion,notas,grupos,grupos_evaluaciones,grupos_integrantes,logs_actividad,materiales,asistencias,asistencia_qr_envios


##  Instalación y Ejecución Local
   **Atención** el repositorio poseé dos carpetas una para el Backend y otra para el Frontend se recomienda una vez clonado el repositorio abrir dos ventanas distintas del IDE que estes       usando, una para el Backend y otra para el Frontend, luego de esto realizar la instalación del entorno virtual y las dependencias, respectivamente para ambas carpetas.
   
   Abajo se muestra un ejemplo para el Backend
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/yapu115/Backend_TP_Integrador.git
   cd Backend_TP_Integrador
   ```
2. **Crear el entorno virtual e instalar dependencias:**
   
   El proyecto incluye un script que crea el entorno virtual y descarga todas las librerías necesarias automáticamente.
   
   ```bash
   cd Backend
   bash init.sh
   source .venv/bin/activate
   ```

3. **Ejecutar la aplicación:**
   ```bash
   cd Backend
   python app.py
   ```

## Documentación de la API(Funcionamiento de endpoints)
La especificación completa de los endpoints se encuentra en el archivo `Backend/docs/swagger.yaml`. Puede ser visualizada gráficamente copiando su contenido en [Swagger Editor](https://editor.swagger.io/) o utilizando una extensión como *Swagger Viewer* en Visual Studio Code.



## Organización del Trabajo
El desarrollo y planificacón del proyecto se gestiona mediante Jira, utilizando metodologías ágiles organizadas en Épicas y Tareas.

## Estado del Proyecto
Finalizado.
