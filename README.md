# Biblioteca

# MySQL
Nombre de la base de datos: **biblioteca**
## Diseñador
![image](https://github.com/Exaedro/biblioteca-app/assets/77593869/951cb361-e297-4a52-a68d-bf4885b44a40)
## Tablas
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
