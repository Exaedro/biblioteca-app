from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class MySQL:
    def __init__(self):
        self.db = mysql.connector.connect(user='root', password='29422196', host='127.0.0.1', database='biblioteca', auth_plugin='mysql_native_password')
        self.cursor = self.db.cursor(buffered=True)
    
    def consulta(self, query, type):
        try:
            self.cursor.execute(query)
        except TypeError:
            return False
        else:
            if(type != 'nonresult'):
                info = self.cursor.fetchone()
                return info 

class App:
    def __init__(self):
        self.app = Tk()
        self.frame = Frame(self.app)
        self.frame.pack()

        self.app.geometry('700x400')
        self.app.title('Biblioteca')

        self.crearInicioDeSesion()

        self.app.mainloop()
        
    def crearInicioDeSesion(self):
        self.usuario = StringVar()
        self.contra = StringVar()
        self.rol = StringVar()

        self.usuario.set('Exaedro')
        self.contra.set('y2k38')

        self.texto1 = ttk.Label(self.frame, text='Usuario', font='bold').grid(column=0, row=0, pady=10)
        self.inpu = ttk.Entry(self.frame, textvariable=self.usuario, width=30).grid(column=0, row=1) # Input del nombre de usuario

        self.texto2 = ttk.Label(self.frame, text='Contraseña', font='bold').grid(column=0, row=2, pady=10)
        self.inpc = ttk.Entry(self.frame, textvariable=self.contra, width=30).grid(column=0, row=3) # Input de la contraseña

        self.boton = ttk.Button(self.frame, text='Iniciar Sesion', command=lambda:self.verificar(), width=30).grid(column=0, row=4, pady=10)

        self.app.mainloop()

    def crearInicio(self):
        self.frame.destroy()

        self.frame = Frame(self.app)
        self.frame.pack(side='left', fill='both')

        self.inicioLabel = ttk.Label(self.frame, text=f"¡Bienvenido {self.usuario.get()}! Eres un {self.rol.get()}.").grid(column=0, row=0)
        self.libro = ttk.Button(self.frame, text='Añadir libro', command=lambda:self.crearLibro()).grid(column=1, row=0)

        self.app.mainloop()
        
    def crearLibro(self):
        self.frame.destroy()

        self.frame = Frame(self.app)
        self.frame.pack(side='left', fill='y')

        self.titulo = StringVar()
        self.autor = StringVar()
        self.anio = StringVar()
        self.disponibilidad = StringVar()

        self.label1 = ttk.Label(self.frame, text='Crear nuevo libro', font='bold').grid(column=0, row=0)
            
        self.label2 = ttk.Label(self.frame, text='Titulo').grid(column=1, row=1)
        self.tituloEntry = ttk.Entry(self.frame, textvariable=self.titulo).grid(column=2, row=1)

        self.label3 = ttk.Label(self.frame, text='Autor').grid(column=1, row=2)
        self.autorEntry = ttk.Entry(self.frame, textvariable=self.autor).grid(column=2, row=2)

        self.label4 = ttk.Label(self.frame, text='Año').grid(column=1, row=3)
        self.anioEntry = ttk.Entry(self.frame, textvariable=self.anio).grid(column=2, row=3)

        self.label5 = ttk.Label(self.frame, text='Disponibilidad').grid(column=1, row=4)
        self.dispEntry = ttk.Combobox(self.frame, state='readonly', values=['Si', 'No'], textvariable=self.disponibilidad).grid(column=2, row=4)

        self.boton1 = ttk.Button(self.frame, text='Añadir libro', command=lambda:self.añadirLibro()).grid(column=5, row=5)

        self.app.mainloop()

    # Funciones que interactuan con la base de datos
    def verificar(self):
        usuario = self.usuario.get()
        contra = self.contra.get()
        db = MySQL()

        if (usuario == '' and contra == ''):
            messagebox.showerror('Error', 'Escribe tus datos para iniciar sesion.')
        elif usuario == '':
            messagebox.showerror('Error', 'Escribe tu nombre de usuario.')
        elif contra == '':
            messagebox.showerror('Error', 'Escribe tu contraseña.')
        else:
            sql = db.consulta(f"SELECT nombre, contra, rol FROM usuarios WHERE nombre = '{usuario}' AND contra = '{contra}'", 'result')

            if(sql != False and sql is not None):
                messagebox.showinfo('Verificado', 'Iniciaste sesion.')
                self.rol.set(sql[2])
                self.crearInicio()
            else:
                messagebox.showerror('Error', 'Datos erroneos.')

    def añadirLibro(self):
        titulo = self.titulo.get()
        autor = self.autor.get()
        anio = self.anio.get()
        disponibilidad = self.disponibilidad.get()
        db = MySQL()

        if(titulo == ''): messagebox.showerror('Error', 'Ingresa el titulo del libro')
        elif(autor == ''): messagebox.showerror('Error', 'Ingresa el autor del libro')
        elif(anio == ''): messagebox.showerror('Error', 'Ingresa el año de publicacion del libro')
        elif(disponibilidad == ''): messagebox.showerror('Error', 'Ingresa si el libro estara disponible')
        else:
            ver = messagebox.askyesno('Añadir Libro', '¿Esta seguro que quiere añadir este libro?')
            if(ver == True):
                if(disponibilidad.lower() == 'si'): disponibilidad = 1
                else: disponibilidad = 0

                sql = f"INSERT INTO libros (titulo, autor, anio, disponibilidad) VALUES ('{titulo}', '{autor}', '{anio}', '{disponibilidad}')"
                db.consulta(sql, 'nonresult')           

app = App()
