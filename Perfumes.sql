CREATE DATABASE IF NOT EXISTS ciber;
USE ciber;

-- 1. Tabla de Usuarios (Actualizada con campos de seguridad)
CREATE TABLE IF NOT EXISTS usuarios (
    usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL, -- Para guardar el hash de Bcrypt
    correo VARCHAR(255),
    perfil VARCHAR(100) NOT NULL DEFAULT 'normal',
    estado ENUM('activo', 'bloqueado') NOT NULL DEFAULT 'activo',
    numeroAccesosErroneo INT NOT NULL DEFAULT 0,
    fechaUltimoAcceso DATE
);

-- 2. Tabla de Perfumes
CREATE TABLE IF NOT EXISTS perfumes (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
    foto VARCHAR(255),
    notas VARCHAR(255)
);

-- 3. Tabla de Comentarios
CREATE TABLE IF NOT EXISTS comentarios (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    FOREIGN KEY (usuario) REFERENCES usuarios(usuario) ON DELETE CASCADE
);

-- ---------------------------------------------------------
-- INSERCIÓN DE DATOS INICIALES
-- ---------------------------------------------------------

-- Usuario Root (Clave '1234' en texto plano para pruebas iniciales)
-- NOTA: Si tu código usa compare_password, este login fallará hasta que 
-- insertes un hash real. Pero para probar la conexión sirve.
INSERT INTO usuarios (usuario, clave, correo, perfil, estado, numeroAccesosErroneo) 
VALUES ('root', '1234', 'admin@ciber.local', 'admin', 'activo', 0)
ON DUPLICATE KEY UPDATE usuario=usuario;

-- Perfume de prueba
INSERT INTO perfumes (nombre, descripcion, precio, foto, notas) 
VALUES ('Sauvage', 'Fragancia Masculina 100ml', 150.00, '/static/Sauvage.png', 'Pimienta, Bergamota, Lavanda');
