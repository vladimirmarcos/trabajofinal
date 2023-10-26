from flask import Flask,render_template,request,redirect,url_for
from form import SignupForm,LoginForm
from flask_login import LoginManager
import os 

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

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  
   
       
    form = LoginForm()
    return render_template('login_form.html', form=form)
        
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))      
       
      