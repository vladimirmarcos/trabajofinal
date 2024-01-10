from flask import render_template, redirect, url_for, request,current_app,flash
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse



from app import login_manager
from . import admin_bp
from .forms import  LoginForm,SignupForm,EliminacionForm,HacerEspecialistaForm,EliminarEspecialistaForm
from .models import AdminUser
from app.user.models_registro_logeo import Useradmin
login_manager.login_view = "admin.ingresar_admin"

from .decorators import admin_required
from . import admin_bp


@admin_bp.route('/admin_ingreso', methods=['GET', 'POST'])
def ingresar_admin():
    """_Funcion de ingreso_

    Returns:
        _type_: _Si ya esta registrado lo manda al la página de usuarios
                 En caso de no estarlo, _
    """

    
    if current_user.is_authenticated:
        return render_template('admin/admin_index.html', user=current_user)
       
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
                    next_page = url_for('admin.index_admin')
                return redirect(next_page)
            else:
                 
                 flash('La contraseña no es la indicada ',"alert alert-danger")
                 return redirect(url_for("admin.ingresar_admin"))
        else:
            userio=form.email.data
            flash( f'El usuario {userio} no esta registrado, como admin. Comuniquese con sistema para solucionar este problema',"alert alert-danger")
            return redirect(url_for("admin.ingresar_admin"))
            
    return render_template('admin/admin_ingreso.html', form=form)

@admin_bp.route("/admin_index", methods=["GET", "POST"])
@admin_required
def index_admin():
    return render_template("admin/admin_index.html")

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


@admin_bp.route("/eliminar_usuarios", methods=["GET", "POST"])
@admin_required
def eliminar_usuario():
    lista=Useradmin.get_all()
    form=EliminacionForm()
    if form.validate_on_submit():
        user = Useradmin.get_by_id(form.id_usuario.data)
        
        if user:
            
            user.delete()
            flash(f'El usuario con el id {form.id_usuario.data} fue eliminado',"alert alert-danger")
            lista=Useradmin.get_all()
            return render_template("admin/eliminar_usuario.html",users=lista,form=form)
        else:
            flash(f'El usuario con el id {form.id_usuario.data} no existe',"alert alert-danger")
            return render_template("admin/eliminar_usuario.html",users=lista,form=form)
    return render_template("admin/eliminar_usuario.html",users=lista,form=form)



@admin_bp.route("/hacer_especialista", methods=["GET", "POST"])
@admin_required
def hacer_especialista():
    
    lista=Useradmin.get_by_algo()
    form=HacerEspecialistaForm()
    
    if not(form.validate_on_submit()):
        user = Useradmin.get_by_id(form.id_usuario.data)
        
        if user:
            
            user.actualizar(form.id_usuario.data,"Especialista")
            
            flash(f'El usuario con el id {form.id_usuario.data} se le asigno el rol de especialista, ahora puede modificar resultados de las T.C.O.',"alert alert-success")
            lista=Useradmin.get_all()
            return render_template("admin/hacer_especialista.html",users=lista,form=form)
        else:
            flash(f'El usuario con el id {form.id_usuario.data} no existe',"alert alert-danger")
            return render_template("admin/hacer_especialista.html",users=lista,form=form)
    return render_template("admin/hacer_especialista.html",users=lista,form=form)

@admin_bp.route("/eliminar_especialista", methods=["GET", "POST"])
@admin_required
def eliminar_especialista():
    
    lista=Useradmin.get_by_especialista()
    form=EliminarEspecialistaForm()
    if form.validate_on_submit():
        user = Useradmin.get_by_id(form.id_usuario.data)
        
        if user:
            
            user.actualizar(form.id_usuario.data,form.usuario_profesion.data)
            flash(f'El usuario con el id {form.id_usuario.data} se le quito el rol de especialista, ahora no puede modificar resultados de las T.C.O.',"alert alert-success")
            lista=Useradmin.get_by_especialista()
            return render_template("admin/eliminar_especialista.html",users=lista,form=form)
        else:
            flash(f'El usuario con el id {form.id_usuario.data} no existe',"alert alert-danger")
            return render_template("admin/eliminar_especialista.html",users=lista,form=form)
    return render_template("admin/eliminar_especialista.html",users=lista,form=form)

@admin_bp.route("/hacer_admin",methods=["GET", "POST"])
@admin_required
def hacer_admin():
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
            flash(f'el usuario {email} fue creado exitosamente',"alert alert-success")
            return render_template("admin/hacer_admin.html", form=form)
     return render_template("admin/hacer_admin.html", form=form)

@admin_bp.route('/logout_admin')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(id):
    return AdminUser.query.get(int(id))