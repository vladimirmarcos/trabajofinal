from flask import Blueprint

servicios_bp = Blueprint('servicios', __name__, template_folder='templates',static_folder='static')

from . import routes