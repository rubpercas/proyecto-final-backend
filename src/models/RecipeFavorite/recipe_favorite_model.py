from .. import db
from sqlalchemy.orm import relationship

class RecetaFavorita(db.Model):   
    __tablename__ = 'receta_favorita'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id', ondelete='CASCADE'), nullable=False)

    usuario = relationship('Usuario', back_populates='favoritas')
    receta = relationship('Receta')

    def __repr__(self):
        return '<RecetaFavorita %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "receta_id": self.receta_id,
            "receta_titulo": self.receta.titulo if self.receta else None
            # do not serialize the password, its a security breach
        }