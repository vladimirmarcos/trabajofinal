from flask import  render_template
from . import public_bp
import logging
logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    """_Index público_

    Returns:
        _type_: _Devuelve la plantilla index público_
    """
    
    return render_template("public/index.html")



