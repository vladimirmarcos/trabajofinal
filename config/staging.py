import os
from .default import *


APP_ENV = APP_ENV_STAGING

SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'medico.db')