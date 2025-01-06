"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models.User.user_model import db, Usuario
from models import Ingrediente, Receta, RecetaFavorita, receta_ingredientes
from routes import user_bp, recipe_bp, ingredient_bp, recipe_favorite_bp
from flask_jwt_extended import JWTManager
from datetime import timedelta
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(recipe_bp, url_prefix='/recipe')
app.register_blueprint(ingredient_bp, url_prefix='/ingredient')
app.register_blueprint(recipe_favorite_bp, url_prefix='/recipe_favorite')

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
flask = JWTManager(app)

jwt_key = os.getenv("JWT_KEY")
app.config["SECRET_KEY"] = jwt_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
