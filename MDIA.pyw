from tkinter import filedialog
from tkinter import *
from functools import partial
import os
import probarImportar


global pathTXT
global pathDATOS


global existe_path_archivo_texto
existe_path_archivo_texto = False

global existe_path_archivo_excel
existe_path_archivo_excel = False

global se_puede_ejecutar
se_puede_ejecutar = False


def ejecutarPrograma():
    if(se_puede_ejecutar):
        print("Programa ejecutado correctamente")
        probarImportar.ejecutarCodigo(pathTXT, pathDATOS)
    else:
        print("No se ejecutó el programa")


def comprobarEjecutar(mi_frame,botonEjecutar):
    global se_puede_ejecutar
    if(existe_path_archivo_texto and existe_path_archivo_excel):
        botonEjecutar.configure(bg="pale green")
        se_puede_ejecutar = True
    else:
        botonEjecutar.configure(bg="red")
        se_puede_ejecutar = False
        print("comprobando falso" + str(existe_path_archivo_texto) + " " + str(existe_path_archivo_excel))

def abrir_archivo_txt(boton, botonEjecutar, mi_frame):
    global existe_path_archivo_texto
    archivo_abierto = filedialog.askopenfilename(initialdir = os.getcwd()+"/", title = "Seleccione archivo", filetypes = (("texto", "*.txt"),("all files")))
    if(archivo_abierto != ""):
        boton.configure(bg="pale green")
        print(archivo_abierto)
        existe_path_archivo_texto = True
    else:
        boton.configure(bg="red")
        existe_path_archivo_texto = False

    global pathTXT
    pathTXT = archivo_abierto
    comprobarEjecutar(mi_frame, botonEjecutar)

def abrir_archivo_excel(boton, botonEjecutar, mi_frame):
    global existe_path_archivo_excel
    archivo_abierto = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Seleccione archivo", filetypes = (("excel", "*.xlsx"),("all files")))
    if(archivo_abierto != ""):
        boton.configure(bg="pale green")
        existe_path_archivo_excel = True
        print(archivo_abierto)
    else:
        boton.configure(bg="red")
        existe_path_archivo_excel = False
    
    global pathDATOS
    pathDATOS = archivo_abierto
    comprobarEjecutar(mi_frame, botonEjecutar)



# creo la interfaz
raiz = Tk()
mi_Frame = Frame(raiz)
mi_Frame.pack()

# creo los elementos
texto1 = Label(mi_Frame, text="Seleccione su archivo de texto")
boton1 = Button(mi_Frame,text = "Abrir archivo de texto")
texto2 = Label(mi_Frame, text="Seleccione su archivo excel modificado")
boton2 = Button(mi_Frame,text = "Abrir archivo excel")
botonEjecutar = Button(mi_Frame, bg = "red", text = "Ejecutar", command = ejecutarPrograma)

boton1.configure(command = partial(abrir_archivo_txt,boton1,botonEjecutar,mi_Frame))
boton2.configure(command = partial(abrir_archivo_excel,boton2,botonEjecutar,mi_Frame)) 
# los posiciono
texto1.grid(row=0, column=0)
boton1.grid(row=1, column=0)
texto2.grid(row=2, column=0)
boton2.grid(row=3, column=0)
botonEjecutar.grid(row = 4,column = 1)

raiz.mainloop()


