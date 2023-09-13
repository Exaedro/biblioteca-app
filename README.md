# Biblioteca

## MySQL - Tablas
Nombre de la base de datos: **biblioteca**
### Usuarios
| Campo          | Tipo     | Longitud |
| -------------- | -------- | -------- |
| id             | int      | null     |
| nombre         | varchar  | 32       |
| contra         | varchar  | 16       |
| rol            | varchar  | 16       |
### Libros
| Campo          | Tipo     | Longitud |
| -------------- | -------- | -------- |
| id             | int      | null     | 
| titulo         | varchar  | 32       | 
| autor          | varchar  | 40       | 
| anio           | varchar  | 5        | 
| disponibilidad | boolean  | 1        |
### Libros prestados
| Campo          | Tipo     | Longitud |
| -------------- | -------- | -------- |
| id             | int      | null     | 
| usuarioId      | varchar  | 40       | 
| libroId        | int      | null     | 
