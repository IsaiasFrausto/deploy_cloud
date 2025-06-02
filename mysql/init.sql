-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS resultados_db;

-- Elimina el usuario si ya existe
DROP USER IF EXISTS 'myuser'@'%';
CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypassword123';
GRANT ALL PRIVILEGES ON resultados_db.* TO 'myuser'@'%';
FLUSH PRIVILEGES;


-- Usar esa base de datos
USE resultados_db;

CREATE TABLE IF NOT EXISTS resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    a FLOAT NOT NULL,
    b FLOAT NOT NULL,
    c FLOAT NOT NULL,
    d FLOAT NOT NULL,
    resultado FLOAT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);