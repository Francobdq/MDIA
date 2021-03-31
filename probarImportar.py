# importo librerias
import os               # para obtener el path de cada archivo
import datetime         # para escribir el tiempo exacto en caso de errores
import pandas as pd     # para el trabajo con dataframes y archivos excel



# Obtengo cada ruta

pathCOPIA = os.getcwd() + '\\data\\txt_con_formato.txt'
pathERRORES = os.getcwd() + "\\data\\errores.txt"
pathOUT = os.getcwd() + '\\output.xlsx'

print(os.getcwd())
#Utiliza el archivo txt ya con el formato dado (separado por ";") y lo convierte en un archivo excel
def exportarExcel(pathTXT, pathOUT):
    excel = pathTXT

    try:
        df = pd.read_csv(excel,sep=';') # lee el archivo excel y separa las columnas por ";"
    except:
        error = "El archivo " + excel + " no existe."
        print(error)
        agregarErrores(error)
        exit()

    column_indexes = list(df.columns)

    df.reset_index(inplace=True)
    df.drop(columns=df.columns[-1], inplace=True)

    column_indexes = dict(zip(list(df.columns),column_indexes))

    df.rename(columns=column_indexes, inplace=True)

    df

    df.to_excel(pathOUT, index = False)
    print("Archivo de texto convertido a excel.")


# Convierte el excel de datos a una lista para poder trabajarlo dentro del programa
def excelALista(pathDATOS, nombreHojaExcel, numFila, numCol):
    excel = pathDATOS

    # lee el excel y separa las columnas con las que se trabajará
    try:
        df = pd.read_excel(excel, nombreHojaExcel)
    except:
        error = "El archivo " + excel + " no existe."
        print(error)
        agregarErrores(error)
        exit()

    df_primerColumna = df.iloc[numFila[0]:,numCol[1]]
    df_segundaColumna = df.iloc[numFila[1]:,numCol[1]]

    #convierte las columnas de dataframe a listas 
    primeraColumna = df_primerColumna.values.tolist()
    segundaColumna = df_segundaColumna.values.tolist()

    # agrega los valores decimales que pide
    cont = 0
    for i in range(len(segundaColumna)):
        if (segundaColumna[i] == 2):
            primeraColumna.insert(i + cont, primeraColumna[i+cont]-2)
            cont += 1

    #Elimina los valores nulos
    primeraColumna = [x for x in primeraColumna if (str(x) != 'nan' and str(x) != ' ')]
    return primeraColumna


# en caso de existir algun error esta funcion se encarga de agregarlo al archivo de texto de errores
def agregarErrores(lineaDeError):
    # abre el archivo de texto de errores
    errores = open(pathERRORES, "a") 
    # obtiene la fecha
    now = datetime.datetime.now()
    # Escribe el error en el archivo de texto
    fechaYhora = ("[" + str(now.date()) + "] [" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] ")
    errores.write(fechaYhora + ":" + lineaDeError + "\n")
    # cierra el archivo de texto
    errores.close()





def ejecutarCodigo(pathTXT, pathDATOS, nombreHojaExcel, numFila, numCol):
    print("ejecutando")

    # abre los archivos de texto
    f2= open(pathCOPIA, "w")

    try:
        f = open(pathTXT, "r+")
    except:
        error = "El archivo " + pathTXT + " no existe."
        print(error)
        agregarErrores(error)
        exit()

    # Obtiene la lista ya convertida
    lista = excelALista(pathDATOS, nombreHojaExcel, numFila, numCol)

    # En la primer linea coloca ";" con espacios vacios (para que la primer linea del txt no sean titulos dentro del excel)
    for j in range(len(lista)+2):
        f2.write(" ;")
    f2.write("\n")


    # reinicia los punteros y obtiene la cantidad de lineas
    f.seek(0)
    cantLineas = len(f.readlines())
    f.seek(0)

    # Recorre cada linea y utilizando la lista para colocar los ";" reescribe todo en un nuevo archivo de texto.
    for j in range(cantLineas):
        linea = f.readline()
        iAnterior = 0
        for i in range(len(lista)):
            f2.write(linea[iAnterior:i] + ";")
            iAnterior = i
        f2.write(linea[iAnterior:-1])
        f2.write(";")
        f2.write(linea[-1])

    # Cierra los txt
    f.close()
    f2.close()

    # Finalmente se crea el excel utilizando este archivo de texto "con formato"
    exportarExcel(pathCOPIA, pathOUT)



#ejecutarCodigo(os.getcwd() + "\\"+ "Deuda009.txt", os.getcwd() + "\\"+ "datos_de_deuda.xlsx")
