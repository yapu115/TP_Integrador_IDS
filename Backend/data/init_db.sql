-- Script potencial, no final

CREATE DATABASE IF NOT EXISTS curso_universitario;
USE curso_universitario;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
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

INSERT INTO tipos_evaluacion (nombre) VALUES ('Parcial'), ('Parcialito'), ('Trabajo Práctico');
INSERT INTO usuarios (username, password_hash, rol) VALUES ('admin', 'hash_de_prueba', 'admin');