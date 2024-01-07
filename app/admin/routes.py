from flask import render_template, redirect, url_for, request,current_app,flash
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse
import os

from app import login_manager,models
from . import admin_bp
from .forms import  LoginForm,SignupForm
from .models import AdminUser



from .decorators import admin_required

from . import admin_bp


@admin_bp.route('/admin_index', methods=['GET', 'POST'])
def ingresar_admin():
    """_Funcion de ingreso_

    Returns:
        _type_: _Si ya esta registrado lo manda al la página de usuarios
                 En caso de no estarlo, _
    """

    
    if current_user.is_authenticated:
        return render_template('admin/admin.html', user=current_user)
       
    form = LoginForm()
    if (form.validate_on_submit()):
        current_app.logger.info(f'{form.correo.data}')
        user = AdminUser.get_by_email(form.correo.data)
        current_app.logger.info(f'{user}')
        if user is not None:
            clave=user.check_password(form.contraseña.data)
            if clave:
                login_user(user, remember=form.remember_me.data)
                
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('admin.crear_admin')
                return redirect(next_page)
            else:
                 current_app.logger.info('La contraseña no es la indicada')
                 flash('La contraseña no es la indicada ',"alert alert-danger")
                 return redirect(url_for("admin.ingresar_admin"))
        else:
            
            userio=form.email.data
            #error =
            current_app.logger.info('el usuario no esta registrado')
            flash( f'El usuario {userio} no esta registrado, como admin. Comuniquese con sistema para solucionar este problema',"alert alert-danger")
            return redirect(url_for("admin.ingresar_admin"))
            
    return render_template('admin/admin_index.html', form=form)

@admin_bp.route("/registrar_admin", methods=["GET", "POST"])
def registrar_admin():
    
    form = SignupForm()
    if form.validate_on_submit():
        
        email = form.correo.data
        password = form.contraseña.data
        user = AdminUser.get_by_email(email)
        if user is not None:
            flash(f'El email {email} ya está siendo utilizado',"alert alert-danger")
            
        else:
            
            user = AdminUser(correo=email,is_admin=True)
            user.set_password(password)
            user.save()
            
            return render_template("admin/registrar.html", form=form)
    return render_template("admin/registrar.html", form=form)


@admin_bp.route("/crear_admin")
@login_required
@admin_required
def crear_admin():
    lista=current_user.get_all()
    
    return render_template("admin/admin.html",users=lista)



@admin_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.crear_admin'))


@login_manager.user_loader
def load_user(id):
    return AdminUser.query.get(int(id))