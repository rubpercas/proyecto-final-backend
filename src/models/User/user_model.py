from .. import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone

class Usuario(db.Model):
    __tablename__ = 'usuarios' 

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    nombre_usuario = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación con Receta
    recetas = relationship('Receta', back_populates='autor', cascade='all, delete-orphan')
    favoritas = relationship('RecetaFavorita', back_populates='usuario')

    def __repr__(self):
        return '<Usuario %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre, 
            "apellidos": self.apellidos,
            "nombre_usuario": self.nombre_usuario,
            "email": self.email,
            # do not serialize the password, its a security breach
        }