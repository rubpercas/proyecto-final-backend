from sqlalchemy import Table, Column, Integer, ForeignKey
from .. import db

# Tabla intermedia para la relación muchos a muchos entre Recetas e Ingredientes
receta_ingredientes = Table(
    'receta_ingredientes',
    db.metadata,
    Column('receta_id', Integer, ForeignKey('recetas.id'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True)
)