from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class ImgForm (FlaskForm):
      id_usuario = IntegerField('dni', validators=[DataRequired(message="el campo es obligarorio")])