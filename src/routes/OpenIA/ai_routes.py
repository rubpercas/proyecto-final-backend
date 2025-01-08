import os
from flask import Blueprint, jsonify, request
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


#  Configurar la API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
#  Cargar variables de entorno
load_dotenv()



ai_bp = Blueprint('ai_bp', __name__)             

# 📌 Generar una receta usando IA
@ai_bp.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "El campo 'prompt' es obligatorio"}), 400
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un chef virtual experto en crear recetas. Responde "
                        "generando una receta completa basada en los ingredientes "
                        "dados. Incluye tiempos de preparación y cocción, lista de "
                        "ingredientes con cantidades, lista de alérgenos, "
                        "información nutricional (hidratos, "
                        "proteínas, grasas y calorías totales) y peso por ración."
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
        return jsonify({"recipe": recipe}), 200

    except openai.OpenAIError as e:
        print("Error con OpenAI:", str(e))
        return jsonify({"error": "Hubo un problema con el servicio de OpenAI"}), 500
    except Exception as e:
        print("Error en el backend:", str(e))
        return jsonify({"error": "Hubo un problema generando la receta"}), 500

