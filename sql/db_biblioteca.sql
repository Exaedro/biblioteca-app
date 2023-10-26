-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-10-2023 a las 22:03:31
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.0.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Base de datos: `db_biblioteca`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id` int(11) NOT NULL,
  `nombre` varchar(55) NOT NULL,
  `genero` varchar(33) NOT NULL,
  `autor` varchar(33) NOT NULL,
  `publicacion` date NOT NULL,
  `edicion` int(11) NOT NULL,
  `rango_edad` enum('ATP','+7','+13','+16','+18') NOT NULL,
  `nro_paginas` int(11) NOT NULL,
  `idioma` varchar(33) NOT NULL,
  `editorial` varchar(33) NOT NULL,
  `nro_de_saga` int(11) NOT NULL,
  `tapa` enum('blanda','dura') NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `librosprestados`
--

CREATE TABLE `librosprestados` (
  `id` int(11) NOT NULL,
  `usuarioId` varchar(40) DEFAULT NULL,
  `LibroId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(32) DEFAULT NULL,
  `contra` varchar(16) DEFAULT NULL,
  `rol` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `contra`, `rol`) VALUES
(0, 'pepe', '123', NULL),
(1, 'admin', '123', 'administrador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `librosprestados`
--
ALTER TABLE `librosprestados`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;
