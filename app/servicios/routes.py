from flask import render_template, redirect, url_for, request,current_app
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse
import os
from app import login_manager
from . import servicios_bp
from .forms import ImgForm,PacienteForm,Informacion
from .models import Imagenes,Diagnostico,Paciente,Fisico
from datetime import date
from .funciones_varias import allowed_file,ALLOWED_EXTENSIONS,red
from werkzeug.utils import secure_filename



@login_required
@servicios_bp.route('/servicios_oculares', methods=['GET', 'POST'])
def servicios_oculares():
    flag=1
    mensaje1="" 
    error=None
    flag=0
    form=ImgForm(request.form)  
    if form.validate_on_submit():
        file=request.files["image"]
        filename= secure_filename(file.filename)
        dni=form.dni.data
        paciente = Paciente.get_by_dni(dni)
        if file and allowed_file(filename) and bool(paciente):
                id_paciente=paciente.id_paciente
                fisico=Fisico.get_by_id_paciente(id_paciente)

                nombre=fisico.nombre
                filename="uploads/"+nombre+"/"+filename
                ruta=os.path.join(current_app.config["UPLOAD_FOLDER"],filename)
                file.save(os.path.join(current_app.config["UPLOAD_FOLDER"],filename))
                img_modelo= os.path.join(current_app.config["UPLOAD_FOLDER"],filename)
                print (img_modelo)
                enfermedades=red(img_modelo)
                caso=Diagnostico(id_paciente=id_paciente,ojo_sano=enfermedades[0],dr=enfermedades[1],crs=enfermedades[2])
                
                imagen=Imagenes(direccion=filename,id_paciente=id_paciente,imagenes_fecha_tomada=date.today())
               
               
                return render_template ('servicios/servicios_oculares.html',flag=0,form=form,mensaje1=enfermedades[0],mensaje2=enfermedades[1],mensaje3=enfermedades[2],name="static/"+filename)
                
        else: 
                error = f'El paciente con {dni} no esta registrado'
                return render_template("servicios/servicios_oculares.html",flag=0,form=form,mensaje1="",mensaje2="",mensaje3="",error=error)
    return render_template("servicios/servicios_oculares.html",flag=0,form=form,mensaje1="",mensaje2="",mensaje3="",error=error)

@login_required   
@servicios_bp.route('/paciente', methods=['GET', 'POST'])
def servicios_paciente():
    error=None
    form=PacienteForm(request.form)
    if form.validate_on_submit():
            nombre = form.name.data
            age = form.edad.data
            h= form.altura.data
            dni=form.dni.data
            peso=form.peso.data
            antecedente=form.antecedente.data
            pas =  Paciente.get_by_dni(dni)
            if pas is not None:
                error = f'El paciente con {dni} ya esta registrado'
                return render_template ('servicios/paciente.html',form=form,error=error)
                
            else:
            # Creamos el usuario y lo guardamos
                paciente=Paciente(dni=dni)
                paciente.save()
                rutas_martin=os.getcwd()
                print(rutas_martin)
                os.chdir("app/static/uploads")
                os.makedirs(nombre)
                os.chdir("../../../")
                error = f'El paciente con {dni} se registro con exito.'
                paciente=Paciente.get_by_dni(dni)
                id_paciente=paciente.id_paciente 
                fisico=Fisico(nombre=nombre,edad=age,altura=h,peso=peso,antecedente=antecedente,id_paciente=id_paciente)
                fisico.save()
                return render_template ('servicios/paciente.html',form=form,error=error)
    return render_template ('servicios/paciente.html',form=form,error=error)    
         
    