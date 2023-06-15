from flask import Flask,render_template,request,redirect,url_for
import os
from form import SignupForm,LoginForm,ImgForm
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_wtf import CSRFProtect
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'medico.db')
app.config["UPLOAD_FOLDER"]="static/uploads"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
csrf=CSRFProtect(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from models import User
from funciones_varias import allowed_file,ALLOWED_EXTENSIONS,red


@app.route('/')
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
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
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
    flag=0
    #comentario para mandar commit con todo funcionando
    if current_user.is_authenticated:
        form=ImgForm(request.form)
        if form.validate_on_submit():
            file=request.files["image"]
            filename= secure_filename(file.filename)
            if file and allowed_file(filename):
                file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
                img_modelo= os.path.join(app.config["UPLOAD_FOLDER"],filename)
                predictions_raw=red(img_modelo)
                return render_template ('mostrar_usuarios.html',mensaje1=predictions_raw[0,0],mensaje2=predictions_raw[0,1],mensaje3=predictions_raw[0,2])
        return render_template("servicios_oculares.html",flag=0,form=form)
    else: 
         
         return render_template("servicios_oculares.html",flag=1)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__=="__main__":
    
    app.run(debug=True)


 