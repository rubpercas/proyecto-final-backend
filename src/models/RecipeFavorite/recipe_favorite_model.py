from .. import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class RecetaFavorita(db.Model):   
    __tablename__ = 'receta_favorita'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id', ondelete='CASCADE'), nullable=False)
    fecha_agregado = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 

    usuario = relationship('Usuario', back_populates='favoritas')
    receta = relationship('Receta')

    def __repr__(self):
        return f'<RecetaFavorita {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "receta_id": self.receta_id,
            "receta_titulo": self.receta.titulo if self.receta else None,
            "fecha_agregado": self.fecha_agregado.isoformat() if self.fecha_agregado else None
        }
