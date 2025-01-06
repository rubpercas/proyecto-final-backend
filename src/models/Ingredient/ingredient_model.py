from .. import db
from ..Associations.receta_ingredientes import receta_ingredientes

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    recetas = db.relationship(
        'Receta',
        secondary=receta_ingredientes,
        back_populates='ingredientes'
    )