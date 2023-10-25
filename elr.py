from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
import mysql.connector

# Buscador
# Cerrar sesion
# Creditos


class MySQL:
    def __init__(self):
        self.db = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="db_biblioteca",
            port="3306",
            auth_plugin="mysql_native_password",
        )
        self.cursor = self.db.cursor(buffered=True)

    def insertIntoUsuarios(self, val):
        consulta = "INSERT INTO usuarios (nombre, contra) VALUES (%s, %s)"
        self.cursor.execute(consulta, val)
        self.db.commit()

    def insertarLibro(self, nombre, genero, autor, publicacion, edicion, rango_edad, nro_paginas, idioma, editorial, nro_de_saga, tapa, disponibilidad):
        consulta = "INSERT INTO libros (nombre, genero, autor, publicacion, edicion, rango_edad, nro_paginas, idioma, editorial, nro_de_saga, tapa, disponibilidad) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (nombre, genero, autor, publicacion, edicion, rango_edad, nro_paginas, idioma, editorial, nro_de_saga, tapa, disponibilidad)

        self.cursor.execute(consulta, val)
        self.db.commit()

    def prestarLibro(self, libroId, usuarioNombre):
        consulta = "INSERT INTO librosprestados (usuarioId, libroId) VALUES (%s, %s)"
        val = (usuarioNombre, libroId)
        self.cursor.execute(consulta, val)
        self.db.commit()

    def devolverLibro(self, libroId, usuarioNombre):
        consulta = f"DELETE FROM librosprestados WHERE libroId = '{libroId}' AND usuarioId = '{usuarioNombre}'"
        self.cursor.execute(consulta)
        self.db.commit()

    def obtenerLibros(self):
        libros = self.consulta("SELECT * FROM libros LIMIT 10")
        return libros

    def editarLibro(self, libroId, nombre, genero, autor, publicacion, edicion, rango_edad, nro_paginas, idioma, editorial, nro_de_saga, tapa, disponibilidad):
        consulta = f"UPDATE libros SET nombre = '{nombre.lower().replace(' ', '-')}', genero = '{genero.lower().replace(' ', '-')}' , autor = '{autor.lower().replace(' ', '-')}', publicacion = '{publicacion}', edicion = '{edicion.lower().replace(' ', '-')}', rango_edad = '{rango_edad.lower()}', nro_paginas = '{nro_paginas}', idioma = '{idioma.lower()}',  ,editorial = '{editorial.lower().replace(' ', '-')}', nro_de_saga = '{nro_de_saga}', tapa = '{tapa}' ,disponibilidad = '{disponibilidad}' WHERE id = '{libroId}'"
        self.cursor.execute(consulta)
        self.db.commit()

    def eliminarLibro(self, libroId):
        consulta = f"DELETE FROM libros WHERE id = {libroId}"
        self.cursor.execute(consulta)
        self.db.commit()

    def obtenerUsuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        resultados = self.cursor.fetchall()
        return resultados

    def consulta(self, query):
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        return resultados


def combine_funcs(*funcs):  # Funcion para ejecutar multiples funciones al mismo tiempo
    def inner_combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return inner_combined_func


class App:
    def __init__(self):
        self.app = Tk()

        # Fuentes para textos
        self.fuenteAlta = Font(family="Roboto Cn", size=14, font="bold")
        self.fuenteBaja = Font(family="Roboto Cn", size=8, font="bold")

        self.app.geometry("500x300")
        self.app.title("PepeLibrary")
        self.app.resizable(width=0, height=1)
    
        self.crearInicioDeSesion()

        self.app.mainloop()

    def crearInicioDeSesion(self):
        self.usuario = StringVar()
        self.contra = StringVar()
        self.rol = StringVar()

        self.usuario.set('admin')
        self.contra.set('123')

        self.frame = Frame(self.app)
        self.frame.pack()

        self.texto1 = ttk.Label(self.frame, text="Usuario", font="bold").grid(
            column=0, row=0, pady=10
        )
        self.inpu = ttk.Entry(self.frame, textvariable=self.usuario, width=30).grid(
            column=0, row=1
        )  # Input del nombre de usuario

        self.texto2 = ttk.Label(self.frame, text="Contraseña", font="bold").grid(
            column=0, row=2, pady=10
        )
        self.inpc = ttk.Entry(self.frame, textvariable=self.contra, width=30).grid(
            column=0, row=3
        )  # Input de la contraseña

        self.boton = ttk.Button(
            self.frame,
            text="Iniciar Sesion",
            command=lambda: self.verificarInicioSesion(),
            width=30,
        ).grid(column=0, row=4, pady=10)
        self.boton2 = ttk.Button(
            self.frame,
            text="Registrarse",
            command=lambda: combine_funcs(self.frame.destroy(), self.crearRegistro()),
            width=30,
        ).grid(column=0, row=5)

        self.app.mainloop()

    def crearRegistro(self):
        self.usuario = StringVar()
        self.contra = StringVar()

        self.frame = Frame(self.app)
        self.frame.pack()

        self.texto1 = ttk.Label(
            self.frame, text="Registro", font=self.fuenteAlta, underline=153
        ).grid(column=0, row=0, pady=30)

        self.textoNombre = ttk.Label(
            self.frame, text="Nombre", font=self.fuenteBaja
        ).grid(column=0, row=1)
        self.entryUsuario = ttk.Entry(
            self.frame, textvariable=self.usuario, width=30
        ).grid(column=0, row=2, pady=10)

        self.textoContra = ttk.Label(
            self.frame, text="Contraseña", font=self.fuenteBaja
        ).grid(column=0, row=3)
        self.entryContra = ttk.Entry(
            self.frame, textvariable=self.contra, width=30
        ).grid(column=0, row=4, pady=10)

        self.botonRegistrarse = ttk.Button(
            self.frame,
            text="Registrarse",
            width=30,
            command=lambda: self.verificarRegistroSesion(),
        ).grid(column=0, row=5
               )
        self.botonCancelar = ttk.Button(
            self.frame,
            text="Cancelar",
            width=30,
            command=lambda: combine_funcs(
                self.frame.destroy(), self.crearInicioDeSesion()
            ),
        ).grid(column=0, row=6, pady=10)

        self.app.mainloop()

    def crearInicio(self):
        self.frame.destroy()

        self.frame = Frame(self.app)
        self.libros = Frame(self.app)
        self.frame.pack(pady=20)
        self.libros.pack(side="left", fill="y", padx=10)

        db = MySQL()

        nombreUsuario = self.usuario.get()
        rolUsuario = self.rol.get()

        # Boton de cerrar sesion
        ttk.Button(self.frame, text='Cerrar sesion', command=lambda: combine_funcs(self.frame.destroy(), self.libros.destroy(), self.crearInicioDeSesion())).grid(column=0, row=0, padx=(0, 60))

        # Texto de bienvenida
        self.inicioLabel = ttk.Label(
            self.frame,
            text=f"¡Bienvenido {nombreUsuario}!",
            font=self.fuenteAlta,
        ).grid(column=1, row=0)

        # Texto de libros disponibles
        self.texto1 = ttk.Label(
            self.libros, text="Libros disponibles", font=self.fuenteAlta
        ).grid(column=0, row=2, pady=10)

        self.busqueda = StringVar()

        ttk.Entry(self.libros, textvariable=self.busqueda).grid(column=0, row=3) # Entry de busqueda
        ttk.Button(self.libros, text='Buscar', command=lambda:self.buscar()).grid(column=1, row=3, padx=10) # Boton de buscar

        libros = db.obtenerLibros()
        if rolUsuario == "administrador":
            # Boton de añadir libro
            self.libro = ttk.Button(
                self.frame, text="Añadir libro", command=lambda: self.crearLibro()
            ).grid(column=2, row=0, padx=3)
            
            # Boton de ver perfil
        ttk.Button(
            self.frame,
            text="Perfil",
            command=lambda: combine_funcs(
                self.frame.destroy(), self.libros.destroy(), self.usuarioPerfil()
            ),
        ).grid(column=3, row=0, padx=3)

        self.app.mainloop()

    def buscar(self):
        self.libros.destroy()
        
        self.libros = Frame(self.app)
        self.libros.pack(side="left", fill="y", padx=10)

        # Texto de libros disponibles
        self.texto1 = ttk.Label(
            self.libros, text="Libros disponibles", font=self.fuenteAlta
        ).grid(column=0, row=2, pady=10)

        ttk.Entry(self.libros, textvariable=self.busqueda).grid(column=0, row=3) # Entry de busqueda
        ttk.Button(self.libros, text='Buscar', command=lambda:self.buscar()).grid(column=1, row=3, padx=10) # Boton de buscar

        db = MySQL()
        busqueda = self.busqueda.get()
        nombreUsuario = self.usuario.get()
        rolUsuario = self.rol.get()

        todosLosLibros = db.consulta(f'SELECT * FROM libros')
        libroBuscado = db.consulta(f'SELECT * FROM libros WHERE nombre = "{busqueda}"')
        
        if(libroBuscado == [] and busqueda == ''): libros = todosLosLibros
        else: libros = libroBuscado
        
        for i in range(len(libros)):
            # Texto del nombre del titulo, autor y año de los libros
            ttk.Label(
                self.libros,
                text=f"{libros[i][1].capitalize().replace('-', ' ')} / {libros[i][2].capitalize().replace('-', ' ')} / {libros[i][3].capitalize().replace('-', ' ')} / {libros[i][4]} / {libros[i][5]} / {libros[i][6]} / {libros[i][7]} / {libros[i][8].capitalize().replace('-', ' ')} / {libros[i][8].capitalize().replace('-', ' ')} / {libros[i][9].capitalize().replace('-', ' ')} / {libros[i][10]} / {libros[i][11].capitalize().replace('-', ' ')}",
            ).grid(column=0, row=i + 4)

            # Boton para pedir prestado
            self.libroBoton = ttk.Button(
                self.libros,
                text="Pedir prestado",
                command=lambda libro=libros[i][0]: self.pedirLibroPrestado(libro),
                state=NORMAL if libros[i][4] else DISABLED,
            ).grid(column=1, row=i + 4, pady=2.5, padx=3)

            if rolUsuario == "administrador":
                # Boton de editar libro
                ttk.Button(
                    self.libros,
                    text="Editar",
                    command=lambda libro=libros[i][0]: combine_funcs(
                        self.frame.destroy(),
                        self.libros.destroy(),
                        self.editarLibro(libro),
                    ),
                ).grid(column=2, row=i + 4)

                #Boton de eliminar libro
                ttk.Button(
                    self.libros,
                    text='Eliminar',
                    command=lambda libroId=libros[i][0]: combine_funcs(
                        self.eliminarLibro(libroId),
                        self.frame.destroy(),
                        self.libros.destroy(),
                        self.crearInicio()
                    )
                ).grid(column=3, row=i+4, padx=3)

    def crearLibro(self):
        self.frame.destroy()
        self.libros.destroy()

        self.frame = Frame(self.app)
        self.formulario = Frame(self.app)
        self.frame.pack()
        self.formulario.pack(padx=20)

        self.nombre = StringVar()
        self.genero = StringVar()
        self.autor = StringVar()
        self.publicacion = StringVar()
        self.edicion = StringVar()
        self.rango_edad = StringVar()
        self.nro_paginas = StringVar()
        self.idioma = StringVar()
        self.editorial = StringVar()
        self.nro_de_saga = StringVar()
        self.tapa = StringVar()
        self.disponibilidad = StringVar()

        self.boton2 = ttk.Button(
            self.frame,
            text="Cancelar",
            padding=5,
            command=lambda: combine_funcs(
                self.formulario.destroy(), self.frame.destroy(), self.crearInicio()
            ),
        ).grid(column=0, row=0)

        self.label1 = ttk.Label(
            self.frame, text="Crear un libro nuevo", font=self.fuenteAlta, padding=15
        ).grid(column=1, row=0)

        self.label2 = ttk.Label(self.formulario, text="nombre", padding=5).grid(
            column=1, row=1
        )
        self.nombreEntry = ttk.Entry(self.formulario, textvariable=self.nombre).grid(
            column=2, row=1
        )

        self.label3 = ttk.Label(self.formulario, text="genero", padding=5).grid(
            column=1, row=2
        )
        self.generoEntry = ttk.Entry(self.formulario, textvariable=self.genero).grid(
            column=2, row=2
        )

        self.label4 = ttk.Label(self.formulario, text="Autor", padding=5).grid(
            column=1, row=3
        )
        self.autorEntry = ttk.Entry(self.formulario, textvariable=self.autor).grid(
            column=2, row=3
        )

        self.label5 = ttk.Label(
            self.formulario, text="Año de publicacion", padding=5
        ).grid(column=1, row=4)
        self.publicacionEntry = ttk.Entry(self.formulario, textvariable=self.publicacion).grid(
            column=2, row=4
        )

        self.label6 = ttk.Label(self.formulario, text="edicion", padding=5).grid(
            column=1, row=5
        )
        self.edicionEntry = ttk.Entry(self.formulario, textvariable=self.edicion).grid(
            column=2, row=5
        )

        self.label7 = ttk.Label(self.formulario, text="rango_edad", padding=5).grid(
            column=1, row=6
        )
        self.rango_edadEntry = ttk.Entry(self.formulario, textvariable=self.rango_edad).grid(
            column=2, row=6
        )

        self.label8 = ttk.Label(self.formulario, text="nro_paginas", padding=5).grid(
            column=1, row=7
        )
        self.nro_paginasEntry = ttk.Entry(self.formulario, textvariable=self.nro_paginas).grid(
            column=2, row=7
        )

        self.label9 = ttk.Label(self.formulario, text="idioma", padding=5).grid(
            column=1, row=8
        )
        self.nro_idiomaEntry = ttk.Entry(self.formulario, textvariable=self.idioma).grid(
            column=2, row=8
        )

        self.label10 = ttk.Label(self.formulario, text="editorial", padding=5).grid(
            column=1, row=9
        )
        self.nro_editorialEntry = ttk.Entry(self.formulario, textvariable=self.editorial).grid(
            column=2, row=9
        )

        self.label11 = ttk.Label(self.formulario, text="nro_de_saga", padding=5).grid(
            column=1, row=10
        )
        self.nro_de_sagaEntry = ttk.Entry(self.formulario, textvariable=self.nro_de_saga).grid(
            column=2, row=10
        )

        self.label12 = ttk.Label(self.formulario, text="tapa", padding=5).grid(
            column=1, row=11
        )
        self.tapaEntry = ttk.Entry(self.formulario, textvariable=self.tapa).grid(
            column=2, row=11
        )

        self.label13 = ttk.Label(self.formulario, text="Disponibilidad", padding=5).grid(
            column=1, row=12
        )
        self.dispEntry = ttk.Combobox(
            self.formulario,
            state="readonly",
            values=["Si", "No"],
            textvariable=self.disponibilidad,
        ).grid(column=2, row=12)

        self.boton1 = ttk.Button(
            self.formulario,
            text="Añadir libro",
            padding=5,
            width=23,
            command=lambda: self.añadirLibro(),
        ).grid(column=2, row=13)

        self.app.mainloop()

    def editarLibro(self, libroId):
        self.nombreFrame = Frame(self.app)
        self.frame = Frame(self.app)
        self.nombreFrame.pack()
        self.frame.pack()

        db = MySQL()
        libroSql = db.consulta(f"SELECT * FROM libros WHERE id = '{libroId}'")

        self.nombre = StringVar(value=libroSql[0][1])
        self.autor = StringVar(value=libroSql[0][2])
        self.anio = StringVar(value=libroSql[0][3])
        self.disponibilidad = StringVar(value=libroSql[0][4])
        libroId = libroSql[0][0]

        ttk.Label(self.nombreFrame, text="Editar libro", font=self.fuenteAlta).grid(
            column=0, row=0, pady=15
        )

        ttk.Label(self.frame, text="Nombre").grid(column=0, row=1)
        ttk.Entry(self.frame, textvariable=self.nombre).grid(column=1, row=1, pady=2.5)

        ttk.Label(self.frame, text="Genero").grid(column=0, row=2)
        ttk.Entry(self.frame, textvariable=self.genero).grid(column=1, row=2, pady=2.5)

        ttk.Label(self.frame, text="Autor").grid(column=0, row=3)
        ttk.Entry(self.frame, textvariable=self.autor).grid(column=1, row=3, pady=2.5)

        ttk.Label(self.frame, text="Publicacion").grid(column=0, row=4)
        ttk.Entry(self.frame, textvariable=self.publicacion).grid(column=1, row=4, pady=2.5)

        ttk.Label(self.frame, text="Edicion").grid(column=0, row=5)
        ttk.Entry(self.frame, textvariable=self.edicion).grid(column=1, row=5, pady=2.5)

        ttk.Label(self.frame, text="Rango de Edad").grid(column=0, row=6)
        ttk.Entry(self.frame, textvariable=self.rango_edad).grid(column=1, row=6, pady=2.5)

        ttk.Label(self.frame, text="Numero de paginas").grid(column=0, row=7)
        ttk.Entry(self.frame, textvariable=self.nro_paginas).grid(column=1, row=7, pady=2.5)

        ttk.Label(self.frame, text="Idioma").grid(column=0, row=8)
        ttk.Entry(self.frame, textvariable=self.idioma).grid(column=1, row=8, pady=2.5)

        ttk.Label(self.frame, text="Editorial").grid(column=0, row=9)
        ttk.Entry(self.frame, textvariable=self.editorial).grid(column=1, row=9, pady=2.5)

        ttk.Label(self.frame, text="Numero de saga").grid(column=0, row=10)
        ttk.Entry(self.frame, textvariable=self.nro_de_saga).grid(column=1, row=10, pady=2.5)

        ttk.Label(self.frame, text="Tapa").grid(column=0, row=11)
        ttk.Entry(self.frame, textvariable=self.tapa).grid(column=1, row=11, pady=2.5)




        ttk.Label(self.frame, text="Disponibilidad").grid(column=0, row=4)
        ttk.Combobox(
            self.frame,
            state="readonly",
            values=["Si", "No"],
            textvariable=self.disponibilidad,
        ).grid(column=1, row=4, pady=2.5)

        ttk.Button(
            self.frame,
            text="Cancelar",
            command=lambda: combine_funcs(
                self.nombreFrame.destroy(), self.crearInicio()
            ),
        ).grid(column=0, row=5)
        ttk.Button(
            self.frame,
            text="Aceptar",
            command=lambda: 
                self.verificarEdicion(
                    libroId,
                    self.nombre.get(),
                    self.autor.get(),
                    self.anio.get(),
                    self.disponibilidad.get(),
                ),
        ).grid(column=1, row=5)

        self.app.mainloop()

    def usuarioPerfil(self):
        self.nombre = Frame()
        self.nombre.pack(pady=20)

        db = MySQL()

        self.libros = Frame()
        self.libros.pack(fill="y", side="left", padx=10)

        ttk.Button(
            self.nombre,
            text="Volver",
            command=lambda: combine_funcs(
                self.nombre.destroy(), self.libros.destroy(), self.crearInicio()
            ),
        ).grid(column=0, row=0)
        ttk.Label(
            self.nombre, text=f"Perfil de {self.usuario.get()}", font=self.fuenteAlta
        ).grid(column=1, row=0)
        ttk.Label(self.libros, text="Tus libros prestados", font=self.fuenteAlta).grid(
            column=0, row=1
        )

        librosSql = db.consulta(
            f"SELECT * FROM libros JOIN librosprestados ON libros.id = librosprestados.libroId WHERE librosprestados.usuarioId = '{self.usuario.get()}'"
        )
        for i in range(len(librosSql)):
            ttk.Label(
                self.libros,
                text=f"{librosSql[i][1].capitalize().replace('-', ' ')} / {librosSql[i][2].capitalize().replace('-', ' ')} / {librosSql[i][3]}",
            ).grid(column=0, row=i + 3, pady=3)
            ttk.Button(
                self.libros,
                text="Devolver libro",
                command=lambda libro=librosSql[i][0]: combine_funcs(
                    self.devolverLibro(libro),
                    self.nombre.destroy(),
                    self.libros.destroy(),
                    self.usuarioPerfil(),
                ),
            ).grid(column=1, row=i + 3, pady=2.5)

    # Funciones que interactuan con la base de datos
    def pedirLibroPrestado(self, libroId):
        db = MySQL()
        usuarioNombre = self.usuario.get()

        sql = db.consulta(
            f"SELECT * FROM librosPrestados WHERE libroId = '{libroId}' AND usuarioId = '{usuarioNombre}'"
        )
        if sql == []:
            db.prestarLibro(libroId, usuarioNombre)
            messagebox.showinfo("Prestado", "Haz pedido prestado este libro.")
        else:
            messagebox.showerror("Error", "Ya tenes este libro.")

    def devolverLibro(self, libroId):
        db = MySQL()
        usuarioNombre = self.usuario.get()

        sql = db.consulta(
            f"SELECT * FROM librosPrestados WHERE libroId = '{libroId}' AND usuarioId = '{usuarioNombre}'"
        )
        if sql == []:
            messagebox.showerror("Error", "Este libro ya lo devolviste.")
        else:
            db.devolverLibro(libroId, usuarioNombre)
            messagebox.showinfo("Exitoso", "Haz devuelto un libro.")

    def eliminarLibro(self, libroId):
        db = MySQL()
        
        ver = messagebox.askyesno('Confirmacion', '¿Esta seguro que quiere eliminar este libro?')
        if(ver == True):
            db.eliminarLibro(libroId)

    def verificarInicioSesion(self):
        usuario = self.usuario.get()
        contra = self.contra.get()
        db = MySQL()

        if usuario == "" and contra == "":
            messagebox.showerror("Error", "Escribe tus datos para iniciar sesion.")
        elif usuario == "":
            messagebox.showerror("Error", "Escribe tu nombre de usuario.")
        elif contra == "":
            messagebox.showerror("Error", "Escribe tu contraseña.")
        else:
            sql = db.consulta(
                f"SELECT nombre, contra, rol FROM usuarios WHERE nombre = '{usuario}' AND contra = '{contra}'"
            )

            if sql != []:
                messagebox.showinfo("Verificado", "Iniciaste sesion.")
                self.rol.set(sql[0][2])
                self.crearInicio()
            else:
                messagebox.showerror("Error", "Datos erroneos.")

    def verificarRegistroSesion(self):
        usuario = self.usuario.get()
        contra = self.contra.get()
        db = MySQL()

        if(usuario == '' and contra == ''):
            messagebox.showerror('Error', 'Ingresa tus datos para registrarte.')
        elif(usuario == ''):
            messagebox.showerror('Error', 'Ingrese su usuario.')
        elif(contra == ''):
            messagebox.showerror('Error', 'Ingrese su contraseña.')
        else:           
            sql = db.consulta(
                f"SELECT nombre, contra FROM usuarios WHERE nombre = '{usuario}' AND contra = '{contra}'"
            )
            
            if sql == []:
                valores = (usuario, contra)
                db.insertIntoUsuarios(valores)
                messagebox.showinfo("Registrado", "Te has registrado correctamente.")
            else:
                messagebox.showerror("Error", "Este usuario ya existe.")

    def verificarEdicion(self, libroId, nombre, genero, autor, publicacion, edicion, rango_edad, nro_paginas, idioma, editorial, nro_de_saga, tapa, disp):
        db = MySQL()

        if nombre == '' and genero == '' and autor == '' and publicacion == '' and edicion == '' and rango_edad == '' and nro_paginas == '' and idioma == '' and editorial == '' and nro_de_saga == '' and tapa == '':
            messagebox.showerror('Error', 'Escribe los datos del libro.')
        elif(nombre == ''):
            messagebox.showerror('Error', 'Escribe el titulo del libro.')
        elif(genero == ''):
            messagebox.showerror('Error', 'Escribe el genero del libro.')
        elif(autor == ''):
            messagebox.showerror('Error', 'Escribe el autor del libro.')
        elif(publicacion == ''):
            messagebox.showerror('Error', 'Escribe el año de publicacion del libro.')
        elif(edicion == ''):
            messagebox.showerror('Error', 'Escribe la edición del libro.')
        elif(rango_edad == ''):
            messagebox.showerror('Error', 'Escribe el rango de edad del libro.')
        elif(nro_paginas == ''):
            messagebox.showerror('Error', 'Escribe el número de paginas del libro.')
        elif(idioma == ''):
            messagebox.showerror('Error', 'Escribe el idioma del libro.')
        elif(editorial == ''):
            messagebox.showerror('Error', 'Escribe la editorial del libro.')
        elif(nro_de_saga == ''):
            messagebox.showerror('Error', 'Escribe el número de saga del libro.')
        elif(tapa == ''):
            messagebox.showerror('Error', 'Escribe el tipo de tapa del libro.')
        elif(disp is int):
            messagebox.showerror('Error', 'Elije si el titulo estara disponible.')



        elif(len(nombre) > 55):
            messagebox.showerror('Error', 'El titulo del libro sobrepasa el limite de caracteres.')
        elif(len(autor) > 33):
            messagebox.showerror('Error', 'El autor del libro sobrepasa el limite de caracteres.')
        elif(len(publicacion) > 4):
            messagebox.showerror('Error', 'El año de publicacion del libro sobrepasa el limite de caracteres.')
        else:
            disp = 1 if disp.lower() == 'si' else 0
            messagebox.showinfo('Editado', 'Libro editado correctamente.')
            db.editarLibro(libroId, nombre, genero, autor, publicacion, edicion, rango_edad, nro_paginas, idioma, editorial, nro_de_saga, tapa, disp)

            self.nombreFrame.destroy()
            self.frame.destroy()
            self.crearInicio()

    def añadirLibro(self):
        nombre = self.nombre.get().lower().replace(" ", "-")
        genero = self.genero.get()
        autor = self.autor.get()
        publicacion = self.publicacion.get()
        edicion = self.edicion.get()
        rango_edad = self.rango_edad.get()
        nro_paginas = self.nro_paginas.get()
        idioma = self.idioma.get()
        editorial = self.editorial.get()
        nro_de_saga = self.nro_de_saga.get()
        tapa = self.tapa.get()
        disponibilidad = self.disponibilidad.get()
        db = MySQL()

        if nombre == "":
            messagebox.showerror("Error", "Ingresa el titulo del libro")
        elif genero == "":
            messagebox.showerror("Error", "Ingresa el genero del libro")
        elif autor == "":
            messagebox.showerror("Error", "Ingresa el autor del libro")
        elif publicacion == "":
            messagebox.showerror("Error", "Ingresa el año de publicacion del libro")
        elif edicion == "":
            messagebox.showerror("Error", "Ingresa la edicion del libro")
        elif rango_edad == "":
            messagebox.showerror("Error", "Ingresa el rango de edad del libro")
        elif nro_paginas == "":
            messagebox.showerror("Error", "Ingresa el número de paginas del libro")
        elif idioma == "":
            messagebox.showerror("Error", "Ingresa el idioma del libro")
        elif editorial == "":
            messagebox.showerror("Error", "Ingresa el editorial del libro")
        elif nro_de_saga == "":
            messagebox.showerror("Error", "Ingresa el número de saga del libro")
        elif tapa == "":
            messagebox.showerror("Error", "Ingresa el tipo de tapa del libro")
        elif disponibilidad == "":
            messagebox.showerror("Error", "Ingresa si el libro estara disponible")
        else:
            sql = db.consulta(f"SELECT nombre FROM libros WHERE nombre = '{nombre}'")
            if sql == []:
                ver = messagebox.askyesno(
                    "Añadir Libro", "¿Esta seguro que quiere añadir este libro?"
                )
                if ver == True:
                    if disponibilidad.lower() == "si":
                        disponibilidad = 1
                    else:
                        disponibilidad = 0

                    db.insertarLibro(nombre, genero, autor, publicacion, edicion, rango_edad, nro_paginas, idioma, editorial, nro_de_saga, tapa, disponibilidad)
            else:
                messagebox.showerror("Error", "Este libro ya existe")

app = App()
