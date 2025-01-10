import os
from flask import Blueprint, jsonify, request
from openai import OpenAI
import openai
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ai_bp = Blueprint('ai_bp', __name__)             

# 📌 Generar una receta usando IA
@ai_bp.route('/generate', methods=['POST'])
def generate_recipe():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "No se proporcionó un prompt"}), 400

    #   Prueba para no gastar tokens.
    #     return jsonify({
    #     "recipe": (
    #         f"Receta generada para los ingredientes: {prompt}\n"
    #         "1. Mezclar los ingredientes.\n"
    #         "2. Cocinar a fuego medio por 20 minutos.\n"
    #         "3. Servir y disfrutar."
    #     )
    # }), 200
    
    # Me daba problema el davinci porque está deprecated, así que usamos el modelo gpt-3.5-turbo
    # Temperature es el estilo de respuesta entre 0 y 1. 0 más predecible, 1 más creativa.
    # max_tokens define el límite máximo de tokens (unidad de texto) que el modelo puede generar en la respuesta.
    # Cada solicitud cuenta con los tokens del prompt y de la respuesta. El modelo (450TK) y el
    # prompt (ej. 50 TK), el coste será de 500 tokens.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un chef virtual experto en crear recetas. Responde "
                        "generando una receta completa basada en los ingredientes dados. "
                        "Incluye el nombre de la receta, una descripción, una lista de ingredientes "
                        "con cantidades, los pasos para prepararla, información nutricional "
                        "(calorías, hidratos, proteínas, grasas), el tiempo de preparación y un enlace "
                        "de imagen. La respuesta debe estar en formato JSON con las siguientes claves:"
                        " 'name', 'image', 'description', 'ingredients', 'steps', 'calories', 'prep_time', 'nutritional values'."
                        "ingredients no quiero que sean objetos, quiero ingrediente y cantidad en un mismo string,"                       
                        "nutritional_values no quiero que sean objetos, quiero un array de strings de respuesta como 'proteins: 25'"
                        "no quiero que generes recetas iguales, quiero que varies"
                    ) 
                },
                {
                    "role": "user",
                    "content": f"Ingredientes: {prompt}"
                }
            ],
            temperature=0.7,
            max_tokens=500)

        # Obtener la respuesta generada por el modelo
        recipe = response.choices[0].message.content.strip()
        print(recipe)
        return jsonify({"recipe": recipe}), 200

    except openai.OpenAIError as e:
        print("Error con OpenAI:", str(e))
        return jsonify({"error": "Hubo un problema con el servicio de OpenAI"}), 500
    except Exception as e:
        print("Error en el backend:", str(e))
        return jsonify({"error": "Hubo un problema generando la receta"}), 500

