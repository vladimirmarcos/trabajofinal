from flask import abort, render_template,current_app
from . import public_bp
from werkzeug.exceptions import NotFound
import logging
logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    current_app.logger.info('Mostrando los posts del blog')
    logger.info('Mostrando los posts del blog')
    return render_template("public/index.html")



