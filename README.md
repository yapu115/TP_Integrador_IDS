# Plataforma de Administración de Cursos Universitarios

Sistema web integral para gestionar en forma completa el ciclo de vida de un curso universitario, abarcando alumnos, evaluaciones, grupos, asistencia, notas y auditoría.

## Integrantes (nombre-legajo)
- Franco Yapura / 115280
- Jean Carlos / 114122
- Federico Andrada de Palomera / 115549
- Franco Miniaci/114868
- Felipe Ricardo Cravero / 114507
- Zlatna Vallejos / 114909

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

El Backend valida las credenciales contra la base de datos usando Werkzeug (para verificar el hash de la contraseña). Si son correctas, genera un JWT firmado con una clave secreta y un tiempo de expiración.

El Backend responde al Frontend con el token JSON. El Frontend almacena este token en la sesión de Flask (session['token']) para mantener al usuario logueado en el navegador de forma segura.
```
Fronten (Cliente)                                          Backend (API REST)
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
## Requisitos previos

- Python 3.10+
- Una instalacion local de MySQL 8
- Linux Ubuntu (Tambien sirve para Mac o en windows habiendo descargado WSL)

#### Instalacion de la base de datos

Si ya tenes MySQL 8 corriendo en tu maquina (puerto `3306` por default):

1. Con los comandos de abajos se crean las tablas y datos de prueba.

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
   source venv/bin/activate
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
