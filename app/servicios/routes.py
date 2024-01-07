from flask import render_template,  request,current_app,redirect, url_for,flash
from flask_login import login_required
from werkzeug.urls import url_parse
import os
from app import login_manager
from . import servicios_bp
from .forms import ImgForm,PacienteForm,Informacion
from .models import Imagenes,Diagnostico,Paciente,Fisico
from datetime import date
from .funciones_varias import allowed_file,ALLOWED_EXTENSIONS,red
from werkzeug.utils import secure_filename
import datetime



@servicios_bp.route('/servicios_oculares', methods=['GET', 'POST'])
@login_required
def servicios_oculares():
    form=ImgForm(request.form)  
    if form.validate_on_submit():
        file=request.files["image"]
        filename= secure_filename(file.filename)
        dni=form.dni.data
        paciente = Paciente.get_by_dni(dni)
        if bool(paciente):
            if file and allowed_file(filename):
                id_paciente=paciente.id_paciente
                fisico=Fisico.get_by_id_paciente(id_paciente)

                nombre=fisico.nombre
                filename="uploads/"+nombre+"/"+filename
                ruta=os.path.join(current_app.config["UPLOAD_FOLDER"],filename)
                file.save(ruta)
                img_modelo= os.path.join(current_app.config["UPLOAD_FOLDER"],filename)
                enfermedades=red(img_modelo)
                suma=enfermedades[0]+enfermedades[1]+enfermedades[2]
                if suma >0.6:
                    fecha=datetime.datetime.now()
                    fecha=datetime.datetime.strftime(fecha,"%Y%m%d")
                    caso=Diagnostico(id_paciente=id_paciente,ojo_sano=enfermedades[0],dr=enfermedades[1],crs=enfermedades[2],fecha_subida=fecha)
                    caso.save()
                
                    imagen=Imagenes(direccion=filename,id_paciente=id_paciente,imagenes_fecha_tomada=date.today())
                    imagen.save()
                    flash("La red recibio satisfactoriamente la imagen. Se muestran los resultados más abajo.","alert alert-success")
                    return render_template ('servicios/servicios_oculares.html',form=form,name="static/"+filename,mensaje=enfermedades)
                else:
                     flash("La red arrojo valores muy bajos, intente subir nuevamente T.C.O. En Caso de que persista el error, comuniquese con el equipo de soporte","alert alert-danger")
                     
                     try:
                            os.remove(ruta)  
                     except FileNotFoundError:
                        print(f"El archivo {ruta} no existe.")
                     except Exception as e:
                            print(f"Error al intentar eliminar el archivo: {e}")
                     return render_template ('servicios/servicios_oculares.html',form=form,name="static/"+filename)
            else: 
               flash(f'El archivo subido no tiene el formato esperado.',"alert alert-danger")
               return render_template("servicios/servicios_oculares.html",form=form,mensaje=None)   
        else:   
                flash(f'El paciente con {dni} no esta registrado. Lo puede hacer en la pestaña de Paciente.',"alert alert-danger")
                return render_template("servicios/servicios_oculares.html",form=form,mensaje=None)
    return render_template("servicios/servicios_oculares.html",form=form)

 
@servicios_bp.route('/paciente', methods=['GET', 'POST'])
@login_required  
def servicios_paciente():
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
                
                flash(f'El paciente con {dni} ya esta registrado',"alert alert-danger")
                return redirect(url_for("servicios.servicios_paciente"))
                
            else:
            # Creamos el usuario y lo guardamos
                paciente=Paciente(dni=dni)
                paciente.save()
                os.chdir("app/static/uploads")
                os.makedirs(nombre)
                os.chdir("../../../")
                paciente=Paciente.get_by_dni(dni)
                id_paciente=paciente.id_paciente 
                fisico=Fisico(nombre=nombre,edad=age,altura=h,peso=peso,antecedente=antecedente,id_paciente=id_paciente)
                fisico.save()
                flash(f'El paciente con nombre {nombre} y D.N.I. {dni} se registro con exito.',"alert alert-success")
                return redirect(url_for("servicios.servicios_paciente"))
    return render_template ('servicios/paciente.html',form=form)    
         
    