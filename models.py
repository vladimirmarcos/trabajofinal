from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    usuario_profesion=db.Column(db.String(128),nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<User {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
class Diagnostico (db.Model, UserMixin):
        __tablename__ = 'imagenes'
        id_imagenes = db.Column(db.Integer, primary_key=True)
        imagenes_archivos = db.Column(db.String(256), nullable=False)
        imagenes_fecha_tomada = db.Column(db.String(256), unique=True, nullable=False)
        ojo_sano = db.Column(db.Float, nullable=False)
        dr = db.Column(db.Float, nullable=False)
        crs = db.Column(db.Float, nullable=False)
        def __repr__(self):
         return f'<diagnostico {self.imagenes_fecha_tomada}>' 
        def save(self):
            if not self.id:
                db.session.add(self)
            db.session.commit()