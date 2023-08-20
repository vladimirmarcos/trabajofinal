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
    

class Imagenes (db.Model, UserMixin):
        __tablename__ = 'imagenes'
        id_imagenes = db.Column(db.Integer, primary_key=True)
        direccion = db.Column(db.String(256), nullable=False)
        id_paciente=db.Column(db.Integer,nullable=False)
        imagenes_fecha_tomada = db.Column(db.String(256), unique=True, nullable=False)
        def __repr__(self):
         return f'<diagnostico {self.imagenes_fecha_tomada}>' 
        def save(self):
            if not self.id_imagenes:
                db.session.add(self)
            db.session.commit()
        @staticmethod
        def get_by_ide(id_paciente):
            return Imagenes.query.filter_by(id_paciente=id_paciente).all()

class Diagnostico (db.Model, UserMixin):
        __tablename__ = 'diagnostico'
        id_diagnostico = db.Column(db.Integer, primary_key=True)
        id_paciente = db.Column(db.Integer, nullable=False)
        ojo_sano = db.Column(db.Float, nullable=False)
        dr = db.Column(db.Float, nullable=False)
        crs = db.Column(db.Float, nullable=False)
        def __repr__(self):
         return f'<diagnostico {self.id_diagnostico}>' 
        def save(self):
            if not self.id_diagnostico:
                db.session.add(self)
            db.session.commit()
        @staticmethod
        def get_by_ide(id_paciente):
            return Diagnostico.query.filter_by(id_paciente=id_paciente).all()

class Paciente (db.Model,UserMixin):
      __tablename__ = 'paciente'
      id_paciente = db.Column(db.Integer, primary_key=True) 
      dni= db.Column(db.Integer, unique=True ,nullable=False)
      def __repr__(self):
         return f'< {self.id_paciente}>'
      def save(self):
            if not self.id_paciente:
             db.session.add(self)
            db.session.commit()
      @staticmethod
      def get_by_dni(dni):
        return Paciente.query.filter_by(dni=dni).first()
    
      
class Fisico (db.Model,UserMixin):
      __tablename__ = 'fisico_paciente'
      id_fisico = db.Column(db.Integer, primary_key=True)
      nombre = db.Column(db.String(256), nullable=False)
      edad= db.Column(db.Integer, nullable=False)
      altura = db.Column(db.Float, nullable=False)
      peso = db.Column(db.Float, nullable=False)
      antecedente = db.Column(db.String(256), nullable=False)
      id_paciente= db.Column(db.Integer, nullable=False)
      
      def __repr__(self):
         return f'<paciente {self.nombre}>'
      def save(self):
            if not self.id_fisico:
             db.session.add(self)
            db.session.commit()
      @staticmethod
      def get_by_id_paciente(paciente):
        return Fisico.query.filter_by(id_paciente=paciente).first()
        
