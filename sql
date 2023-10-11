CREATE DATABASE db_biblioteca;
USE db_biblioteca;

CREATE TABLE usuarios(
	id INT PRIMARY KEY,
	nombre VARCHAR(32),
    contra VARCHAR(16),
    rol VARCHAR (16)
);

CREATE TABLE libros(
	id INT PRIMARY KEY,
    titulo VARCHAR(32),
    autor VARCHAR(40),
    anio INT(5),
    disponibilidad BOOLEAN
);

CREATE TABLE librosprestados(
	id INT PRIMARY KEY,
    usuarioId VARCHAR(40),
    LibroId	INT(11)
);
