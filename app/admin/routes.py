from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse


from app import login_manager
from . import admin_bp
from app.user.forms import SignupForm, LoginForm





from .decorators import admin_required
from app import login_manager
from . import admin_bp

@admin_bp.route("/algo")
@login_required
@admin_required
def algo():
    return(render_template("/admin/admin.html"))