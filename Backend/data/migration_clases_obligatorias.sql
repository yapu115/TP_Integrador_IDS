USE curso_universitario;

CREATE TABLE IF NOT EXISTS clases_obligatorias (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    nombre_clase VARCHAR(100) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
