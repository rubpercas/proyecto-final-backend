from flask import Blueprint, request, jsonify
from models.Ingredient.ingredient_model import Ingrediente, db

ingredient_bp = Blueprint('ingredient_bp', __name__)

# 📌 Obtener todos los ingredientes
@ingredient_bp.route('/', methods=['GET'])
def get_ingredients():
    ingredientes = Ingrediente.query.all()
    return jsonify([{
        "id": ingrediente.id,
        "nombre": ingrediente.nombre
    } for ingrediente in ingredientes]), 200

# 📌 Crear un nuevo ingrediente
@ingredient_bp.route('/create', methods=['POST'])
def create_ingredient():
    data = request.json
    
    # Validar que el nombre está presente
    if 'nombre' not in data or not data['nombre']:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    
    new_ingredient = Ingrediente(
        nombre=data['nombre']
    )
    db.session.add(new_ingredient)
    db.session.commit()
    return jsonify({"message": "Ingrediente creado correctamente"}), 201

# 📌 Obtener un ingrediente por ID
@ingredient_bp.route('/<int:id>', methods=['GET'])
def get_ingredient_by_id(id):
    ingrediente = Ingrediente.query.get(id)
    if not ingrediente:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    
    return jsonify({
        "id": ingrediente.id,
        "nombre": ingrediente.nombre
    }), 200

# 📌 Actualizar un ingrediente
@ingredient_bp.route('/<int:id>', methods=['PUT'])
def update_ingredient(id):
    ingrediente = Ingrediente.query.get(id)
    if not ingrediente:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    
    data = request.json
    ingrediente.nombre = data.get('nombre', ingrediente.nombre)

    db.session.commit()
    return jsonify({"message": "Ingrediente actualizado correctamente"}), 200

# 📌 Eliminar un ingrediente
@ingredient_bp.route('/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
    ingrediente = Ingrediente.query.get(id)
    if not ingrediente:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    
    db.session.delete(ingrediente)
    db.session.commit()
    return jsonify({"message": "Ingrediente eliminado correctamente"}), 200

# 📌 Obtener todas las recetas que contienen un ingrediente
@ingredient_bp.route('/<int:id>/recetas', methods=['GET'])
def get_recipes_by_ingredient(id):
    ingrediente = Ingrediente.query.get(id)
    if not ingrediente:
        return jsonify({"error": "Ingrediente no encontrado"}), 404

    return jsonify([{
        "id": receta.id,
        "titulo": receta.titulo,
        "descripcion": receta.descripcion
    } for receta in ingrediente.recetas]), 200