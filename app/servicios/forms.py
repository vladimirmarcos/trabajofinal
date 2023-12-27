from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FileField,IntegerField,DecimalField,TextAreaField
from wtforms.validators import DataRequired, Length


class ImgForm (FlaskForm):
      image =FileField('image')
      dni = IntegerField('dni', validators=[DataRequired(message="el campo es obligarorio")])
      

class PacienteForm(FlaskForm):
        dni = IntegerField('dni', validators=[DataRequired(message="el campo es obligarorio")])
        submit = SubmitField('Registrar')
        name = StringField('Nombre', validators=[DataRequired(message="el campo es obligatorio"), Length(min=3,max=64,message="El campo es oblogatorio y debe tener entre 3 a 64 caracteres")])
        edad = IntegerField('edad', validators=[DataRequired(message="el campo es obligarorio")])
        altura = DecimalField('Altura', validators=[DataRequired()])
        peso = DecimalField('Peso', validators=[DataRequired()])
        antecedente=TextAreaField ('Antecedentes', validators=[DataRequired()])  


class Informacion(FlaskForm):
      dni = IntegerField('dni', validators=[DataRequired(message="el campo es obligarorio")])
