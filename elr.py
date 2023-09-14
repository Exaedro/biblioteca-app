from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
import mysql.connector


class MySQL:
    def __init__(self):
        self.db = mysql.connector.connect(
            user="root",
            password="",
            host="127.0.0.1",
            database="biblioteca",
            port='3306',
            auth_plugin="mysql_native_password",
        )
        self.cursor = self.db.cursor(buffered=True)

    def insertIntoUsuarios(self, val):
        consulta = "INSERT INTO usuarios (nombre, contra) VALUES (%s, %s)"
        self.cursor.execute(consulta, val)
        self.db.commit()

    def insertarLibro(self, titulo, autor, anio, disp):
        consulta = "INSERT INTO libros (titulo, autor, anio, disponibilidad) VALUES (%s, %s, %s, %s)"
        val = (titulo, autor, anio, disp)

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

    def editarLibro(self, libroId, titulo, autor, anio, disp):
        disp = 1 if disp.lower() == "si" else 0
        consulta = f"UPDATE libros SET titulo = '{titulo.lower().replace(' ', '-')}', autor = '{autor.lower().replace(' ', '-')}', anio = '{anio}', disponibilidad = '{disp}' WHERE id = '{libroId}'"
        self.cursor.execute(consulta)
        self.db.commit()

    def eliminarLibro(self, libroId):
        consulta = f"delete from libros where id = '{libroId}'"
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
        self.app.title("Biblioteca")

        self.crearInicioDeSesion()

        self.app.mainloop()

    def crearInicioDeSesion(self):
        self.usuario = StringVar()
        self.contra = StringVar()
        self.rol = StringVar()

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
            text="Registrase",
            width=30,
            command=lambda: self.verificarRegistroSesion(),
        ).grid(column=0, row=5)
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

        self.inicioLabel = ttk.Label(
            self.frame,
            text=f"¡Bienvenido {nombreUsuario}!",
            font=self.fuenteAlta,
        ).grid(column=0, row=0)
        self.texto1 = ttk.Label(
            self.libros, text="Libros disponibles", font=self.fuenteAlta
        ).grid(column=0, row=2)

        libros = db.obtenerLibros()
        for i in range(len(libros)):
            ttk.Label(
                self.libros,
                text=f"{libros[i][1].capitalize().replace('-', ' ')} / {libros[i][2].capitalize().replace('-', ' ')} / {libros[i][3]}",
            ).grid(column=0, row=i + 3)
            self.libroBoton = ttk.Button(
                self.libros,
                text="Pedir prestado",
                command=lambda libro=libros[i][0]: self.pedirLibroPrestado(libro),
                state=NORMAL if libros[i][4] else DISABLED,
            ).grid(column=1, row=i + 3, pady=2.5, padx=3)
            if rolUsuario == "administrador":
                ttk.Button(
                    self.libros,
                    text="Editar",
                    command=lambda libro=libros[i][0]: combine_funcs(
                        self.frame.destroy(),
                        self.libros.destroy(),
                        self.editarLibro(libro),
                    ),
                ).grid(column=2, row=i + 3)
                ttk.Button(
                    self.libros,
                    text='Eliminar',
                    command=lambda libroId=libros[i][0]: combine_funcs(
                        self.eliminarLibro(libroId),
                        self.libros.destroy(),
                        self.crearInicio()
                    )
                ).grid(column=3, row=i+3, padx=3)

        if rolUsuario == "administrador":
            self.libro = ttk.Button(
                self.frame, text="Añadir libro", command=lambda: self.crearLibro()
            ).grid(column=1, row=0, padx=3)
        ttk.Button(
            self.frame,
            text="Perfil",
            command=lambda: combine_funcs(
                self.frame.destroy(), self.libros.destroy(), self.usuarioPerfil()
            ),
        ).grid(column=2, row=0, padx=3)

        self.app.mainloop()

    def crearLibro(self):
        self.frame.destroy()
        self.libros.destroy()

        self.frame = Frame(self.app)
        self.formulario = Frame(self.app)
        self.frame.pack()
        self.formulario.pack(padx=20)

        self.titulo = StringVar()
        self.autor = StringVar()
        self.anio = StringVar()
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

        self.label2 = ttk.Label(self.formulario, text="Titulo", padding=5).grid(
            column=1, row=1
        )
        self.tituloEntry = ttk.Entry(self.formulario, textvariable=self.titulo).grid(
            column=2, row=1
        )

        self.label3 = ttk.Label(self.formulario, text="Autor", padding=5).grid(
            column=1, row=2
        )
        self.autorEntry = ttk.Entry(self.formulario, textvariable=self.autor).grid(
            column=2, row=2
        )

        self.label4 = ttk.Label(
            self.formulario, text="Año de publicacion", padding=5
        ).grid(column=1, row=3)
        self.anioEntry = ttk.Entry(self.formulario, textvariable=self.anio).grid(
            column=2, row=3
        )

        self.label5 = ttk.Label(self.formulario, text="Disponibilidad", padding=5).grid(
            column=1, row=4
        )
        self.dispEntry = ttk.Combobox(
            self.formulario,
            state="readonly",
            values=["Si", "No"],
            textvariable=self.disponibilidad,
        ).grid(column=2, row=4)

        self.boton1 = ttk.Button(
            self.formulario,
            text="Añadir libro",
            padding=5,
            width=23,
            command=lambda: self.añadirLibro(),
        ).grid(column=2, row=5)

        self.app.mainloop()

    def editarLibro(self, libroId):
        self.tituloFrame = Frame(self.app)
        self.frame = Frame(self.app)
        self.tituloFrame.pack()
        self.frame.pack()

        db = MySQL()
        libroSql = db.consulta(f"SELECT * FROM libros WHERE id = '{libroId}'")

        self.titulo = StringVar(value=libroSql[0][1])
        self.autor = StringVar(value=libroSql[0][2])
        self.anio = StringVar(value=libroSql[0][3])
        self.disponibilidad = StringVar(value=libroSql[0][4])
        libroId = libroSql[0][0]

        ttk.Label(self.tituloFrame, text="Editar libro", font=self.fuenteAlta).grid(
            column=0, row=0, pady=15
        )

        ttk.Label(self.frame, text="Titulo").grid(column=0, row=1)
        ttk.Entry(self.frame, textvariable=self.titulo).grid(column=1, row=1, pady=2.5)

        ttk.Label(self.frame, text="Autor").grid(column=0, row=2)
        ttk.Entry(self.frame, textvariable=self.autor).grid(column=1, row=2, pady=2.5)

        ttk.Label(self.frame, text="Año de publicacion").grid(column=0, row=3)
        ttk.Entry(self.frame, textvariable=self.anio).grid(column=1, row=3, pady=2.5)

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
                self.tituloFrame.destroy(), self.crearInicio()
            ),
        ).grid(column=0, row=5)
        ttk.Button(
            self.frame,
            text="Aceptar",
            command=lambda: combine_funcs(
                self.tituloFrame.destroy(),
                self.frame.destroy(),
                db.editarLibro(
                    libroId,
                    self.titulo.get(),
                    self.autor.get(),
                    self.anio.get(),
                    self.disponibilidad.get(),
                ),
                self.crearInicio(),
            ),
        ).grid(column=1, row=5)

        self.app.mainloop()

    def usuarioPerfil(self):
        self.titulo = Frame()
        self.titulo.pack(pady=20)

        db = MySQL()

        self.libros = Frame()
        self.libros.pack(fill="y", side="left", padx=10)

        ttk.Button(
            self.titulo,
            text="Volver",
            command=lambda: combine_funcs(
                self.titulo.destroy(), self.libros.destroy(), self.crearInicio()
            ),
        ).grid(column=0, row=0)
        ttk.Label(
            self.titulo, text=f"Perfil de {self.usuario.get()}", font=self.fuenteAlta
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
                    self.titulo.destroy(),
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

            if sql != False and sql is not None:
                messagebox.showinfo("Verificado", "Iniciaste sesion.")
                self.rol.set(sql[0][2])
                self.crearInicio()
            else:
                messagebox.showerror("Error", "Datos erroneos.")

    def verificarRegistroSesion(self):
        usuario = self.usuario.get()
        contra = self.contra.get()
        db = MySQL()

        sql = db.consulta(
            f"SELECT nombre, contra FROM usuarios WHERE nombre = '{usuario}' AND contra = '{contra}'"
        )
        if sql == []:
            elpepe = (usuario, contra)
            db.insertIntoUsuarios(elpepe)
            messagebox.showinfo("Registrado", "Te has registrado correctamente.")
        else:
            messagebox.showerror("Error", "Este usuario ya existe.")

    def añadirLibro(self):
        titulo = self.titulo.get().lower().replace(" ", "-")
        autor = self.autor.get()
        anio = self.anio.get()
        disponibilidad = self.disponibilidad.get()
        db = MySQL()

        if titulo == "":
            messagebox.showerror("Error", "Ingresa el titulo del libro")
        elif autor == "":
            messagebox.showerror("Error", "Ingresa el autor del libro")
        elif anio == "":
            messagebox.showerror("Error", "Ingresa el año de publicacion del libro")
        elif disponibilidad == "":
            messagebox.showerror("Error", "Ingresa si el libro estara disponible")
        else:
            sql = db.consulta(f"SELECT titulo FROM libros WHERE titulo = '{titulo}'")
            print(sql)
            if sql == []:
                ver = messagebox.askyesno(
                    "Añadir Libro", "¿Esta seguro que quiere añadir este libro?"
                )
                if ver == True:
                    if disponibilidad.lower() == "si":
                        disponibilidad = 1
                    else:
                        disponibilidad = 0

                    db.insertarLibro(titulo, autor, anio, disponibilidad)
            else:
                messagebox.showerror("Error", "Este libro ya existe")

    def eliminarLibro(self, libroId):
        db = MySQL()
        
        verificar = db.consulta(f"select * from libros where id = '{libroId}'")
        if(verificar == []):
            messagebox.showerror('Error', 'Este libro ya fue borrado o no existe')
        else:
            per = messagebox.askyesno('Confirmacion', '¿Estas seguro que queres eliminar este libro?')
            db.eliminarLibro(libroId) if per == 1 else 0

app = App()
