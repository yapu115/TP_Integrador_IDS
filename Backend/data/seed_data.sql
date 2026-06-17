USE curso_universitario;

-- Alumnos de prueba
INSERT IGNORE INTO alumnos (legajo, nombre, apellido, email, abandono, curso_id) VALUES
('62001', 'Juan', 'Pérez', 'jperez@fi.uba.ar', FALSE, 1),
('62002', 'María', 'González', 'mgonzalez@fi.uba.ar', FALSE, 1),
('62003', 'Carlos', 'López', 'clopez@fi.uba.ar', FALSE, 1),
('62004', 'Ana', 'Martínez', 'amartinez@fi.uba.ar', FALSE, 1),
('62005', 'Pedro', 'Rodríguez', 'prodriguez@fi.uba.ar', TRUE, 1),
('62006', 'Laura', 'Fernández', 'lfernandez@fi.uba.ar', FALSE, 1),
('62007', 'Diego', 'Ramírez', 'dramirez@fi.uba.ar', FALSE, 1),
('62008', 'Sofía', 'Torres', 'storres@fi.uba.ar', TRUE, 1),
('62009', 'Lucas', 'Díaz', 'ldiaz@fi.uba.ar', FALSE, 1),
('62010', 'Valentina', 'Castro', 'vcastro@fi.uba.ar', FALSE, 1);

-- Notas de prueba (id_evaluacion: 1=Parcial, 2=Parcialito, 3=Trabajo Práctico)
INSERT IGNORE INTO notas (id_alumno, id_evaluacion, nota) VALUES
-- Parcial
(1, 1, 8.5), (2, 1, 6.0), (3, 1, 4.0), (4, 1, 9.0), (5, 1, 2.0),
(6, 1, 7.5), (7, 1, 5.5), (9, 1, 3.5), (10, 1, 8.0),
-- Parcialito
(1, 2, 7.0), (2, 2, 5.0), (3, 2, 6.5), (4, 2, 9.5), (6, 2, 8.0),
(7, 2, 4.5), (9, 2, 6.0), (10, 2, 7.5),
-- Trabajo Práctico
(1, 3, 9.0), (2, 3, 7.0), (3, 3, 8.0), (4, 3, 10.0), (6, 3, 8.5),
(7, 3, 6.0), (9, 3, 7.5), (10, 3, 9.0);

-- Grupos (equipos) de prueba
INSERT IGNORE INTO grupos (id, nombre_grupo, curso_id) VALUES
(1, 'Los Binarios', 1),
(2, 'Los Algorítmicos', 1);

INSERT IGNORE INTO grupo_evaluaciones (id_grupo, id_evaluacion) VALUES
(1, 3),
(2, 3);

INSERT IGNORE INTO grupo_integrantes (id_grupo, id_alumno) VALUES
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 6), (2, 7), (2, 9), (2, 10);
