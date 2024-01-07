from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

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
        fecha_subida=db.Column(db.String(256), nullable=False)
        fecha_modificada=db.Column(db.String(256))
        quien_modifico=db.Column(db.String(256))

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