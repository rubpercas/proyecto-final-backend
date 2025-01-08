from flask import Blueprint, request, jsonify
from models.RecipeFavorite.recipe_favorite_model import RecetaFavorita
from models.Recipe.recipe_model import Receta
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

favorite_bp = Blueprint('favorite_bp', __name__)

# 📌 Añadir receta a favoritos
@favorite_bp.route('/add', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.json
    receta_id = data.get('receta_id')
    
    if not receta_id:
        return jsonify({"error": "Se requiere el ID de la receta"}), 400
    
    # Validar existencia de receta
    receta = Receta.query.get(receta_id)
    if not receta:
        return jsonify({"error": "La receta no existe"}), 404
    
    # Validar si ya está en favoritos
    exists = RecetaFavorita.query.filter_by(usuario_id=user_id, receta_id=receta_id).first()
    if exists:
        return jsonify({"message": "La receta ya está en favoritos"}), 400
    
    new_fav = RecetaFavorita(usuario_id=user_id, receta_id=receta_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "Receta añadida a favoritos"}), 201

# 📌 Eliminar receta de favoritos
@favorite_bp.route('/remove', methods=['DELETE'])
@jwt_required()
def remove_favorite():
    user_id = get_jwt_identity()
    data = request.json
    receta_id = data.get('receta_id')
    
    fav = RecetaFavorita.query.filter_by(usuario_id=user_id, receta_id=receta_id).first()
    if not fav:
        return jsonify({"error": "La receta no está en favoritos"}), 404
    
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Receta eliminada de favoritos"}), 200
