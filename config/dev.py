from .default import *
import os
import sqlalchemy

APP_ENV = APP_ENV_DEVELOPMENT

SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'medico.db')
print ("direcion de base datos")
print(os.path.join(basedir, 'medico.db'))