from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField,IntegerField
from wtforms.validators import DataRequired, Email
class LoginForm(FlaskForm):
    correo = StringField('Email    ', validators=[DataRequired(message="el campo es obligatorio")])
    contraseña= PasswordField('Password', validators=[DataRequired("el campo es obligatorio")])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Ingresar')
    

class SignupForm(FlaskForm):
    correo = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message="el campo es obligarorio")])
    submit = SubmitField('Registrar')  

class EliminacionForm(FlaskForm):
    id_usuario= IntegerField('ID de usuario a eliminar', validators=[DataRequired(message="el campo es obligarorio")])
    submit = SubmitField('Eliminar')  


class HacerEspecialistaForm(FlaskForm):
    id_usuario= IntegerField('ID de usuario hacer especialista', validators=[DataRequired(message="el campo es obligarorio")])
    submit = SubmitField('Hacer')  