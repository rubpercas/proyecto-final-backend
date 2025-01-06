from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User.user_model import Usuario
from .Recipe.recipe_model import Receta
from .Ingredient.ingredient_model import Ingrediente
from .RecipeFavorite.recipe_favorite_model import RecetaFavorita
from .Associations.receta_ingredientes import receta_ingredientes