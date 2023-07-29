from flask import Flask,render_template,request,redirect,url_for
import os
import random
from form import SignupForm,LoginForm,ImgForm,PacienteForm
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_wtf import CSRFProtect
import matplotlib.pyplot as plt
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
global_numero=0
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'medico.db')
app.config["UPLOAD_FOLDER"]="static/uploads"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
csrf=CSRFProtect(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from models import User,Diagnostico,Paciente
from funciones_varias import allowed_file,ALLOWED_EXTENSIONS,red


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        usuario_profesion=form.usuario_profesion.data
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            
            user = User(name=name, email=email,usuario_profesion=usuario_profesion)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)

@app.route('/servicios_oculares', methods=['GET', 'POST'])
def servicios_oculares():
    flag=1
    mensaje1=""
    arreglo=['sano','dr','scr']
    colores = ["#EE6055","#60D394","#AAF683"]
    arreglo_resultados=[]
    #comentario para mandar commit con todo funcionando
    if current_user.is_authenticated:
        flag=0
        form=ImgForm(request.form)
        if form.validate_on_submit():
            file=request.files["image"]
            filename= secure_filename(file.filename)
            if file and allowed_file(filename):
                file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
                img_modelo= os.path.join(app.config["UPLOAD_FOLDER"],filename)
                predictions_raw=red(img_modelo)
                algo=list(predictions_raw[0][0])
                
                s=algo[0]
                dr=algo[1]
                scr=algo[2]
                arreglo_resultados.append(s)
                arreglo_resultados.append(dr)
                arreglo_resultados.append(scr)
                numero=random.randrange(1, 1000, 2)
               
                caso=Diagnostico(imagenes_archivos=img_modelo,imagenes_fecha_tomada="sadas",ojo_sano=s,dr=dr,crs=scr)
                caso.save()
                plt.pie(arreglo_resultados, labels=arreglo,colors=colores)
                
                name ="static/graficos/Ejemplo"+str(numero)+ ".jpg"
                
                #plt.savefig(name)
                name="graficos/Ejemplo"+str(numero)+ ".jpg"
                return render_template ('servicios_oculares.html',flag=0,form=form,mensaje1=s,mensaje2=dr,mensaje3=scr,name=name)
        return render_template("servicios_oculares.html",flag=0,form=form,mensaje1="",mensaje2="",mensaje3="")
    else: 
         
         return render_template("servicios_oculares.html",flag=1)



@app.route('/paciente', methods=['GET', 'POST'])
def servicios_paciente():
    error=None

    if current_user.is_authenticated :
        form=PacienteForm(request.form)
        if form.validate_on_submit():
            nombre = form.name.data
            age = form.edad.data
            h= form.altura.data
            dni=form.dni.data
            pas =  Paciente.get_by_dni(dni)
            if pas is not None:
                error = f'El paciente con {dni} ya esta registrado'
                
            else:
            # Creamos el usuario y lo guardamos
                paciente=Paciente(nombre=nombre,edad=age,dni=dni,altura=h)
                paciente.save()
                os.chdir("static/uploads")
                os.makedirs(nombre)
                os.chdir("../../")
                error = f'El paciente con {dni} se registro con exito.'
                return render_template ('paciente.html',form=form,error=error)
            
         
    return render_template("paciente.html",form=form,error=error)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__=="__main__":
    
    app.run(debug=True)


 