USE curso_universitario;

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
