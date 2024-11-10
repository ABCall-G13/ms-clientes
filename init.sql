CREATE DATABASE IF NOT EXISTS clientes;

USE clientes;

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL UNIQUE,
    nit VARCHAR(60) NOT NULL UNIQUE,
    direccion VARCHAR(60),
    telefono VARCHAR(60),
    industria VARCHAR(60),
    password VARCHAR(128) NOT NULL,
    WelcomeMessage VARCHAR(255),
    escalation_time INT,
    plan ENUM('Emprendedor', 'Empresario', 'Empresario Plus') DEFAULT NULL,  -- Campo `plan` agregado
    INDEX (nombre),
    INDEX (email),
    INDEX (nit)
);
