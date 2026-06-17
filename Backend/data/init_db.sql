drop database curso_universitario;

CREATE DATABASE IF NOT EXISTS curso_universitario;
USE curso_universitario;


CREATE TABLE IF NOT EXISTS usuarios (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    username         VARCHAR(50) NOT NULL UNIQUE,
    email            VARCHAR(100) NOT NULL UNIQUE,
    password_hash    VARCHAR(255) NOT NULL,
    rol              ENUM('admin', 'profesor') DEFAULT 'profesor',
    ultimo_acceso    DATETIME,
    activo           BOOLEAN DEFAULT TRUE,
    fecha_creacion   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cursos (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    descripcion      TEXT,
    fecha_inicio     DATE,
    fecha_fin        DATE,
    activo           BOOLEAN DEFAULT TRUE,
    fecha_creacion   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS alumnos (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    curso_id         INT NOT NULL,
    legajo           VARCHAR(20) NOT NULL,
    nombre           VARCHAR(100) NOT NULL,
    apellido         VARCHAR(100) NOT NULL,
    email            VARCHAR(100) NOT NULL,
    abandono         BOOLEAN DEFAULT FALSE,
    fecha_registro   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_legajo_curso (legajo, curso_id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS tipos_evaluacion (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    nombre           VARCHAR(50) NOT NULL,
    descripcion      TEXT,
    fecha            DATE,
    hora             TIME
);


CREATE TABLE IF NOT EXISTS notas (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno        INT NOT NULL,
    id_evaluacion    INT NOT NULL,
    nota             DECIMAL(4,2),
    fecha_carga      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_nota_alumno_evaluacion (id_alumno, id_evaluacion),
    FOREIGN KEY (id_alumno)     REFERENCES alumnos(id)          ON DELETE CASCADE,
    FOREIGN KEY (id_evaluacion) REFERENCES tipos_evaluacion(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS grupos (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    curso_id         INT NOT NULL,
    nombre_grupo     VARCHAR(50) NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS grupo_evaluaciones (
    id_grupo         INT,
    id_evaluacion    INT,
    PRIMARY KEY (id_grupo, id_evaluacion),
    FOREIGN KEY (id_grupo)      REFERENCES grupos(id)           ON DELETE CASCADE,
    FOREIGN KEY (id_evaluacion) REFERENCES tipos_evaluacion(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS grupo_integrantes (
    id_grupo         INT,
    id_alumno        INT,
    PRIMARY KEY (id_grupo, id_alumno),
    FOREIGN KEY (id_grupo)  REFERENCES grupos(id)  ON DELETE CASCADE,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS logs_actividad (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    usuario          VARCHAR(50) NOT NULL,
    accion           VARCHAR(255) NOT NULL,
    detalles         TEXT,
    fecha            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS materiales (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    curso_id         INT NOT NULL,
    titulo           VARCHAR(255) NOT NULL,
    url_archivo      VARCHAR(255) NOT NULL,
    fecha_subida     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS asistencias (
    id_asistencia    INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno        INT NOT NULL,
    fecha            DATE NOT NULL,
    estado           VARCHAR(20) NOT NULL DEFAULT 'presente',
    codigo_qr        VARCHAR(255) NOT NULL,
    creado_en        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_alumno_fecha (id_alumno, fecha),
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS asistencia_qr_envios (
    id_envio         INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno        INT NOT NULL,
    curso_id         INT NOT NULL,
    fecha            DATE NOT NULL,
    codigo_qr        VARCHAR(255) NOT NULL,
    destinatario     VARCHAR(100) NOT NULL,
    enviado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_qr_envio_alumno_fecha (id_alumno, fecha),
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);


INSERT IGNORE INTO tipos_evaluacion (nombre,descripcion,fecha,hora) VALUES
    ('Parcial','Evaluación de mitad de cuatrimestre', '2026-06-20', '10:00:00'),
    ('Parcialito','Evaluación corta de lectura', '2026-06-25', '14:30:00'),
    ('Trabajo Práctico','Entrega de proyecto grupal', '2026-07-01', '23:59:00');

INSERT IGNORE INTO usuarios (username, email, password_hash, rol, activo)
VALUES (
    'admin',
    'admin@fi.uba.ar',
    'scrypt:32768:8:1$oBmzlHyWpksghi0Y$bb052984618802029759b2ac1fb186076fe7cc7ecad4c3da04bb2e0c5923ae0548269cf05698927f8c9e7dbce387c1c35dc6fc72609e985da4defc0800748266', -- admin123
    'admin',
    TRUE
);

-- Curso de ejemplo
INSERT IGNORE INTO cursos (id, nombre, descripcion) VALUES
    (1, 'Introducción al Desarrollo de Software', 'Curso de primer año');

-- Alumnos de ejemplo asignados al curso 1
INSERT IGNORE INTO alumnos (legajo, nombre, apellido, email, curso_id) VALUES
    ('1001', 'Juan',  'Pérez', 'jperez@fi.uba.ar',  1),
    ('1002', 'María', 'Gómez', 'mgomez@fi.uba.ar',  1);
