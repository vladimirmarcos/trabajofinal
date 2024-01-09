from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Useradmin(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    usuario_profesion=db.Column(db.String(128),nullable=False)

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
        return Useradmin.query.get(id)
    
    @staticmethod
    def get_by_email(email):
        try:
            return Useradmin.query.filter_by(email=email).first()
        except:
            return None
    @staticmethod
    def get_all():
        return Useradmin.query.all()
    
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def actualizar(self,id_usuario,profesion):
        user = Useradmin.get_by_id(id_usuario)

        user.usuario_profesion = profesion
        db.session.commit()

    @staticmethod
    def get_by_algo(valor="Especialista"):
        return Useradmin.query.filter(Useradmin.usuario_profesion!=valor).all()

       
    @staticmethod
    def get_by_especialista(valor="Especialista"):
        return Useradmin.query.filter(Useradmin.usuario_profesion==valor).all()
  
    


        
