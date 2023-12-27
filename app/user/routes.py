from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse


from app import login_manager
from . import user_bp
from .forms import SignupForm, LoginForm
from .models import User


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    error=None
    user=None
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
       
    form = LoginForm()
    if (form.validate_on_submit()):
        
        user = User.get_by_email(form.email.data)
        if user is not None:
            clave=user.check_password(form.password.data)
            if clave:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('user.index')
                return redirect(next_page)
            else:
                 error = f'La contraseña no es la indicada '
                 return render_template('user/login_form.html', form=form,error=error,user=user)
        else:
            #print (user.check_passaword(form.password.data)) 
            userio=form.email.data
            error = f'El usuario {userio} no esta registrado'
            return render_template('user/login_form.html', form=form,error=error,user=user)
    return render_template('user/login_form.html', form=form,error=error,user=user)

@user_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
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
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template("user/signup_form.html", form=form, error=error)

@user_bp.route('/user', methods=['GET', 'POST'])
@login_required

def index():
    return render_template("user/index_user.html")
@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
