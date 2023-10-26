from flask import Flask,render_template,request,redirect,url_for
from form import SignupForm,LoginForm
from flask_login import LoginManager,logout_user, current_user, login_user
import os 
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'medico.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)

db = SQLAlchemy(app)
from models import User
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    user=None
    if current_user.is_authenticated:
        return redirect(url_for('index'))
       
    form = LoginForm()
    if (form.validate_on_submit()):
        
        user = User.get_by_email(form.email.data)
        if user is not None:
            clave=user.check_password(form.password.data)
            if clave:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
            else:
                 error = f'La contraseña no es la indicada D: '
                 return render_template('login_form.html', form=form,error=error,user=user)
        else:
            #print (user.check_passaword(form.password.data)) 
            userio=form.email.data
            error = f'El usuario {userio} no esta registrado'
            return render_template('login_form.html', form=form,error=error,user=user)
    return render_template('login_form.html', form=form,error=error,user=user)

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
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('login')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)
        
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))      
       
      
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))