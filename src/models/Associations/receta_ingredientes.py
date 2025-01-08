from sqlalchemy import Table, Column, Integer, ForeignKey
from .. import db

receta_ingredientes = db.Table(
    'receta_ingredientes',
    db.Column('receta_id', db.Integer, db.ForeignKey('recetas.id', ondelete='CASCADE'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingredientes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('cantidad', db.String(50), nullable=True)  # Cantidad específica del ingrediente
)
