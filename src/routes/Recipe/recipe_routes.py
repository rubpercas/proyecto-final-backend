from flask import Blueprint, request, jsonify
from models.Recipe.recipe_model import Receta, db

recipe_bp = Blueprint('recipe_bp', __name__)

# Obtener todas las recetas
@recipe_bp.route('/', methods=['GET'])
def get_recipes():
    recipes = Receta.query.all()
    return jsonify([recipe.titulo for recipe in recipes]), 200

# Crear una nueva receta
@recipe_bp.route('/create', methods=['POST'])
def create_recipe():
    data = request.json
    
    # Validar que usuario_id esté presente y no sea nulo
    if 'usuario_id' not in data or not data['usuario_id']:
        return jsonify({"error": "El campo 'usuario_id' es obligatorio"}), 400

    # Validar que el usuario existe
    from models.User.user_model import Usuario
    usuario = Usuario.query.get(data['usuario_id'])
    if not usuario:
        return jsonify({"error": "El usuario especificado no existe"}), 404

     # Filtrar datos válidos para evitar errores con claves inesperadas
    allowed_fields = { 
        "id", "usuario_id", "titulo", "descripcion", "pasos",
        "foto_url", "calorias", "nutrientes", "tiempo_elaboracion"
    }
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    
    # Crear la receta usando **filtered_data
    new_recipe = Receta(**filtered_data)
    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify({"message": "Receta creada correctamente", "id": new_recipe.id}), 201


@recipe_bp.route('/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    receta = Receta.query.get(id)
    if not receta:
        return jsonify({"error": "Receta no encontrada"}), 404
    return jsonify({"receta":receta.serialize()}), 200



# 📌 Actualizar una receta por ID
@recipe_bp.route('/<int:id>', methods=['PUT'])
def update_recipe(id):
    receta = Receta.query.get(id)
    if not receta:
        return jsonify({"error": "Receta no encontrada"}), 404
    
    data = request.json
    receta.titulo = data.get('titulo', receta.titulo)
    receta.descripcion = data.get('descripcion', receta.descripcion)
    receta.pasos = data.get('pasos', receta.pasos)
    receta.foto_url = data.get('foto_url', receta.foto_url)
    receta.calorias = data.get('calorias', receta.calorias)
    receta.nutrientes = data.get('nutrientes', receta.nutrientes)
    receta.tiempo_elaboracion = data.get('tiempo_elaboracion', receta.tiempo_elaboracion)

    db.session.commit()
    return jsonify({"message": "Receta actualizada correctamente"}), 200

# 📌 Eliminar una receta por ID
@recipe_bp.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    receta = Receta.query.get(id)
    if not receta:
        return jsonify({"error": "Receta no encontrada"}), 404

    db.session.delete(receta)
    db.session.commit()
    return jsonify({"message": "Receta eliminada correctamente"}), 200


# 📌 Obtener todas las recetas de un usuario específico
@recipe_bp.route('/user/<int:usuario_id>', methods=['GET'])
def get_recipes_by_user(usuario_id):
    recetas = Receta.query.filter_by(usuario_id=usuario_id).all()
    if not recetas:
        return jsonify({"error": "No se encontraron recetas para este usuario"}), 404
    
    return jsonify([{
        "id": receta.id,
        "titulo": receta.titulo,
        "descripcion": receta.descripcion,
        "autor_id": receta.usuario_id
    } for receta in recetas]), 200

