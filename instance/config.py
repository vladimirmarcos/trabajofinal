import os 
from os.path import abspath, dirname

SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

basedir = dirname(dirname(abspath(__file__)))

SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'medico.db')