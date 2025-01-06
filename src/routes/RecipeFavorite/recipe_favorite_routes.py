from flask import Blueprint, request, jsonify
from models.RecipeFavorite.recipe_favorite_model import RecetaFavorita, db
from models.User.user_model import Usuario
from models.Recipe.recipe_model import Receta

recipe_favorite_bp = Blueprint('recipe_favorite_bp', __name__)


# Obtener todas las recetas favoritas
@recipe_favorite_bp.route('/', methods=['GET'])
def get_all_favorites():
    favorites = RecetaFavorita.query.all()
    return jsonify([
        {"usuario_id": fav.usuario_id, "receta_id": fav.receta_id} 
        for fav in favorites
    ]), 200

# Añadir una receta a favoritos
@recipe_favorite_bp.route('/create', methods=['POST'])
def add_favorite():
    data = request.json
    
    # Validar que usuario_id y receta_id estén presentes
    if 'usuario_id' not in data or 'receta_id' not in data:
        return jsonify({"error": "Se requiere 'usuario_id' y 'receta_id'"}), 400
    
    # Validar que el usuario existe
    usuario = Usuario.query.get(data['usuario_id'])
    if not usuario:
        return jsonify({"error": "El usuario especificado no existe"}), 404

    # Validar que la receta existe
    receta = Receta.query.get(data['receta_id'])
    if not receta:
        return jsonify({"error": "La receta especificada no existe"}), 404
    
    # Validar que la relación no exista previamente
    favorito_existente = RecetaFavorita.query.filter_by(
        usuario_id=data['usuario_id'], 
        receta_id=data['receta_id']
    ).first()
    if favorito_existente:
        return jsonify({"error": "Esta receta ya está en favoritos para este usuario"}), 400

    # Crear una nueva relación favorita
    new_favorite = RecetaFavorita(
        usuario_id=data['usuario_id'],
        receta_id=data['receta_id']
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Receta añadida a favoritos"}), 201

# Obtener las recetas favoritas de un usuario específico
@recipe_favorite_bp.route('/user/<int:usuario_id>', methods=['GET'])
def get_user_favorites(usuario_id):
    favoritos = RecetaFavorita.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([
        {"receta_id": fav.receta_id}
        for fav in favoritos
    ]), 200

# Eliminar una receta de favoritos
@recipe_favorite_bp.route('/', methods=['DELETE'])
def delete_favorite():
    data = request.json
    
    if 'usuario_id' not in data or 'receta_id' not in data:
        return jsonify({"error": "Se requiere 'usuario_id' y 'receta_id'"}), 400

    favorito = RecetaFavorita.query.filter_by(
        usuario_id=data['usuario_id'],
        receta_id=data['receta_id']
    ).first()
    
    if not favorito:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Receta eliminada de favoritos"}), 200