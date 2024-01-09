from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin'
    id= db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(256), unique=True, nullable=False)
    contraseña= db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return f'<User {self.correo}>'
    
    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id_admin):
        return AdminUser.query.get(id_admin)
    
    @staticmethod
    def get_by_email(correo):
        
            return AdminUser.query.filter_by(correo=correo).first()
        
    @staticmethod
    def get_all():
        return AdminUser.query.all()
    
    
    

