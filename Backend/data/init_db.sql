CREATE DATABASE IF NOT EXISTS curso_universitario;
USE curso_universitario;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'profesor') DEFAULT 'profesor',
    ultimo_acceso DATETIME,
    activo BOOLEAN DEFAULT TRUE,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    legajo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    abandono BOOLEAN DEFAULT FALSE, 
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tipos_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
    -- Faltan alumnos asociados a las evaluaciones?
);



CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT,
    id_evaluacion INT,
    nota DECIMAL(4,2),
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_evaluacion) REFERENCES tipos_evaluacion(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_equipo VARCHAR(50),
    id_tp INT,
    FOREIGN KEY (id_tp) REFERENCES tipos_evaluacion(id)
);

CREATE TABLE IF NOT EXISTS equipo_integrantes (
    id_equipo INT,
    id_alumno INT,
    PRIMARY KEY (id_equipo, id_alumno),
    FOREIGN KEY (id_equipo) REFERENCES equipos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS asistencias (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'presente',
    codigo_qr VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_alumno_fecha (id_alumno, fecha),

    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE
);

INSERT IGNORE INTO tipos_evaluacion (nombre) VALUES 
('Parcial'), 
('Parcialito'), 
('Trabajo Práctico');

INSERT IGNORE INTO usuarios (username, email, password_hash, rol, activo) 
VALUES (
    'admin', 
    'admin@fi.uba.ar', 
    'scrypt:32768:8:1$oBmzlHyWpksghi0Y$bb052984618802029759b2ac1fb186076fe7cc7ecad4c3da04bb2e0c5923ae0548269cf05698927f8c9e7dbce387c1c35dc6fc72609e985da4defc0800748266', -- admin123
    'admin',
    TRUE
);
