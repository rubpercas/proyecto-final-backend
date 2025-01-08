from .. import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..Associations.receta_ingredientes import receta_ingredientes

class Receta(db.Model):
    __tablename__ = 'recetas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    pasos = db.Column(db.Text)
    foto_url = db.Column(db.String(255))
    calorias = db.Column(db.Integer)
    nutrientes = db.Column(db.Text)
    tiempo_elaboracion = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    popularidad = db.Column(db.Integer, default=0)  
    visibilidad = db.Column(db.String(10), default='publica')  # 'publica' o 'privada'
    origen = db.Column(db.String(50), default='usuario')  # 'usuario' o 'ia'

    autor = relationship('Usuario', back_populates='recetas')
    ingredientes = relationship('Ingrediente', secondary=receta_ingredientes, back_populates='recetas')
    favoritas = relationship('RecetaFavorita', back_populates='receta', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Receta {self.titulo}>'

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "pasos": self.pasos,
            "foto_url": self.foto_url,
            "calorias": self.calorias,
            "nutrientes": self.nutrientes,
            "tiempo_elaboracion": self.tiempo_elaboracion,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "popularidad": self.popularidad,
            "visibilidad": self.visibilidad,
            "origen": self.origen
        }
