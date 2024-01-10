from flask import render_template, redirect, url_for, request,current_app,flash
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse
from app import login_manager
from . import user_bp
from .forms import SignupForm, LoginForm
from .models_registro_logeo import Useradmin


@user_bp.route('/ingresar', methods=['GET', 'POST'])
def login():
    """_Funcion de ingreso_

    Returns:
        _type_: _Si ya esta registrado lo manda al la página de usuarios
                 En caso de no estarlo, _
    """

    
    if current_user.is_authenticated:
        return render_template('user/index_user.html', user=current_user)
       
    form = LoginForm()
    if (form.validate_on_submit()):
        
        user = Useradmin.get_by_email(form.email.data)
        if user is not None:
            clave=user.check_password(form.password.data)
            if clave:
                login_user(user, remember=form.remember_me.data)
                succes_message="Bienvenido{}".format(user.name)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('user.index')
                return redirect(next_page)
            else:
                 current_app.logger.info('La contraseña no es la indicada')
                 flash('La contraseña no es la indicada ',"alert alert-danger")
                 return redirect(url_for("user.login"))
        else:
            
            userio=form.email.data
            #error =
            current_app.logger.info('el usuario no esta registrado')
            flash( f'El usuario {userio} no esta registrado',"alert alert-danger")
            return redirect(url_for("user.login"))
            
    return render_template('user/ingresar.html', form=form)

@user_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        usuario_profesion=form.usuario_profesion.data
        user = Useradmin.get_by_email(email)
        if user is not None:
            flash(f'El email {email} ya está siendo utilizado',"alert alert-danger")
            
        else:
            user = Useradmin(name=name, email=email,usuario_profesion=usuario_profesion)
            user.set_password(password)
            user.save()
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('user.index')
            return redirect(next_page)
    return render_template("user/registrar.html", form=form)

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
    return Useradmin.get_by_id(int(user_id))
