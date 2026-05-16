# Plataforma de Administración de Cursos Universitarios

Sistema web integral para gestionar en forma completa el ciclo de vida de un curso universitario, abarcando alumnos, evaluaciones, grupos, asistencia, notas y auditoría.

## Integrantes (nombre-legajo)
- Franco Yapura / 115280
- xxx / xxx

## Características Principales

El sistema cumple con el alcance mínimo requerido para el Trabajo Práctico Integrador:

*   **Seguridad y Auditoría:**
    *   Autenticación de usuarios mediante tokens (JWT/Bearer).
    *   Manejo de usuarios (Administradores/Profesores) y registro de actividad (log) del sistema.
*   **Gestión de Alumnos:**
    *   ABM completo de alumnos.
    *   Importación masiva de alumnos mediante archivos CSV.
    *   Control de estado de los alumnos (seguimiento de abandono de la materia).
*   **Evaluaciones y Notas:**
    *   ABM de tipos de evaluación (Parciales, Parcialitos, Trabajos Prácticos, etc.).
    *   Sistema de carga y registro de calificaciones para todos los tipos de evaluación.
*   **Gestión de Equipos (Grupos):**
    *   ABM de equipos integrados por "n" alumnos.
    *   Asociación dinámica de equipos a uno o varios Trabajos Prácticos.
*   **Asistencia Inteligente:**
    *   Sistema de asistencia mediante generación de códigos QR dinámicos.
    *   Referencia directa al alumno y la fecha específica.
    *   Envío automatizado del código QR por correo electrónico.
*   **Dashboard e Informes (PDF):**
    *   Listado de alumnos con filtros dinámicos.
    *   Estadísticas generales de aprobación.
    *   Listado de equipos conformados.
*   **Características Adicionales:**
    *   Sección para carga de material de estudio (visualización pública sin autenticación, y gestión protegida).
    *   Proyecto completamente Dockerizado para fácil despliegue.

##  Tecnologías Utilizadas

*   **Backend:** Python 3, Flask
*   **Base de Datos:** MySQL
*   **Frontend:** HTML5, CSS3, JavaScript
*   **Documentación de API:** Swagger (`Backend/docs/swagger.yaml`)

##  Instalación y Ejecución Local

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

4. **Ejecutar la aplicación:**
   ```bash
   cd Backend
   python app.py
   ```

## Documentación de la API
La especificación completa de los endpoints se encuentra en el archivo `Backend/docs/swagger.yaml`. Puede ser visualizada gráficamente copiando su contenido en [Swagger Editor](https://editor.swagger.io/) o utilizando una extensión como *Swagger Viewer* en Visual Studio Code.

## Organización del Trabajo
El desarrollo y planificación del proyecto se gestiona mediante Jira, utilizando metodologías ágiles organizadas en Épicas y Tareas.

## Estado del Proyecto
En Desarrollo: Iterando sobre las funcionalidades base, documentación de API y configuración de base de datos.