from flask import Flask,render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import logging
from logging.handlers import SMTPHandler
login_manager = LoginManager()
db = SQLAlchemy()

   
def create_app(settings_module):
    """_summary_:función principal

    Args:
        settings_module (configuracion): _este argumento te dice como va a trabajar la app_

    Returns:
        _type_: _description_
    """
    app = Flask(__name__, instance_relative_config=True)
    # Load the config file specified by the APP environment variable
    app.config.from_object(settings_module)
    app.config["MODEL_FOLDER"]="app/static/models/" 
    app.config["UPLOAD_FOLDER"]="app/static/"
    # Load the configuration from the instance folder
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)
    
    
    
    login_manager.init_app(app)
    

    db.init_app(app)

    # Registro de los Blueprints
    from .public import public_bp
    app.register_blueprint(public_bp)

    from .user import user_bp
    app.register_blueprint(user_bp)

    from .servicios import servicios_bp
    app.register_blueprint(servicios_bp)

    

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    register_error_handlers(app)
    return app



def register_error_handlers(app):
    """_Funcion para manejo de errores_

    Args:
        app (Aplicacion): _description_

    Returns:
        _type_: _description_
    """
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500
    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404
    @app.errorhandler(401)
    def error_404_handler(e):
        return render_template('401.html'), 401
    
def configure_logging(app):
    """_Configuración de loggs de la app _

    Args:
        app (_type_): _description_
    """
    del app.logger.handlers[:]

    loggers = [app.logger, ]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   app.config['DONT_REPLY_FROM_EMAIL'],
                                   app.config['ADMINS'],
                                   '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
                                   (app.config['MAIL_USERNAME'],
                                    app.config['MAIL_PASSWORD']),
                                   ())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d

            Message:

            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )