from .default import *
import os

# Parámetros para activar el modo debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING

SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'medico.db')
