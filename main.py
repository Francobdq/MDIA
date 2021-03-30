import os
import logging
import probarImportar
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

from werkzeug.middleware.shared_data import SharedDataMiddleware
#
UPLOAD_FOLDER = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


logging.basicConfig(level=logging.DEBUG)
logging.debug("Log habilitad!")


def allowed_file(filename, tipo):
    ALLOWED_EXTENSIONS = {tipo}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def manejoDeArchivo(archivo):
    f = open(archivo, 'r')
    f.seek(0)
    logging.debug(f.readline())




@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        if 'excel' not in request.files:
            flash('No file apart')
            return redirect(request.url)
        


        file = request.files['file']
        excel = request.files['excel']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, "txt"):
            filenameTXT = "Deuda.txt"
            pathTXT = os.path.join(app.config['UPLOAD_FOLDER'], filenameTXT)
            file.save(pathTXT)
            #manejoDeArchivo(pathTXT)
            
            if excel.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if excel and allowed_file(excel.filename, "xlsx"):
                filenameXLSX = "datos_de_deuda.xlsx"
                pathXLSX = os.path.join(app.config['UPLOAD_FOLDER'], filenameXLSX)
                excel.save(pathXLSX)

                probarImportar.ejecutarCodigo(pathTXT, pathXLSX)
                nombreOUT = 'output.xlsx'
                return redirect(url_for('uploaded_file',
                                        filename=nombreOUT))



    return render_template("index.html")



app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})
