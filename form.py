from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField,FileField,SelectField
from wtforms.validators import DataRequired, Email, Length
class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(message="el campo es obligatorio"), Length(min=3,max=64,message="El campo es oblogatorio y debe tener entre 3 a 64 caracteres")])
    password = PasswordField('Password', validators=[DataRequired(message="el campo es obligarorio")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    usuario_profesion=SelectField('usuario_profesion',choices=[('medico','medico'),('especialista','especialista'),("enfermero","enfermero")])
    submit = SubmitField('Registrar')  
pais = SelectField('País', choices=[('AR', 'Argentina'), ('AT', 'Austria'), ('AU', 'Australia')])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="el campo es obligatorio")])
    password = PasswordField('Password', validators=[DataRequired("el campo es obligatorio")])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Ingresar')


class ImgForm (FlaskForm):
      image =FileField('image')


