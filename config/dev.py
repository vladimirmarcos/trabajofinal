from .default import *
import os

APP_ENV = APP_ENV_DEVELOPMENT

SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'medico.db')