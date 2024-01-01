from flask import render_template, redirect, url_for, request
from flask_login import login_required
from werkzeug.urls import url_parse
import os

from app import login_manager,models
from . import admin_bp
from app.user.forms import SignupForm, LoginForm
#from models import User_admin



from .decorators import admin_required
from app import login_manager
from . import admin_bp
#from models import Useradmin

@admin_bp.route("/algo")
@login_required
@admin_required
def algo():
    #lista=current_user.get_all()
    #print (lista)
    return(render_template("admin/admin.html"))


