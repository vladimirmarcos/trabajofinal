from flask import  render_template,current_app
from . import public_bp
import logging
logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    current_app.logger.info('Mostrando los posts del blog')
    return render_template("public/index.html")



