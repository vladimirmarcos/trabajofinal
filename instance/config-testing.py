import os 
from os.path import abspath, dirname



basedir = dirname(dirname(abspath(__file__)))

SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'medico.db')