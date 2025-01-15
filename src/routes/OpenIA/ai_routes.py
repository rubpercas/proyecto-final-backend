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
                            "Eres un chef virtual experto en crear recetas creativas y deliciosas. Genera una receta completa que incluya:"
                            "- Nombre de la receta (clave: name)"
                            "- Descripción apetitosa de la receta (clave: description)"
                            "- Lista de ingredientes con cantidades precisas, en un array de strings (clave: ingredients)"
                            "- Pasos detallados para preparar la receta (clave: steps)"
                            "- Cantidad de calorías totales (clave: calories)"
                            "- Información nutricional (hidratos de carbono, proteínas, grasas), cada valor como un string en el formato nutrient: value (clave: nutritional_values)"
                            "- Tiempo de preparación (clave: prep_time)"
                            "- Para el campo image, incluye una combinación creativa de 2-3-4 emojis que representen visualmente el plato. Por ejemplo:"
                            "* Para una pizza:" "🍕👨‍🍳"
                            "* Para un postre de chocolate:" "🍫🎂✨"
                            "* Para una ensalada:" "🥗🥬🥕"
                            "* Para una sopa:" "🥣🥘🌶️"
                            "* Para un plato de pasta:" "🍝🧀🌿"
                            "* Para un plato de pescado:" "🐟🍋🌊"
                            "* Para un plato de carne:" "🥩🔥🌿"
                            "* Para un desayuno:" "🍳🥓🥖"

                            "La respuesta debe estar en formato JSON con las siguientes claves: name, image, description, ingredients, steps, calories, prep_time, y nutritional_values. Los ingredientes deben estar en formato de texto, no como objetos, y los valores nutricionales deben ser un array de strings en lugar de objetos. Asegúrate de variar las recetas generadas para que no se repitan."

                            "Sé creativo con las combinaciones de emojis, adaptándolas al plato específico y sus ingredientes principales."
                        # "Eres un chef virtual experto en crear recetas. Genera una receta completa basada en los ingredientes que te proporciono. La receta debe incluir lo siguiente:"
                        # "Nombre de la receta (clave: name)."
                        # "Descripción de la receta (clave: description)."
                        # "Lista de ingredientes con cantidades, en un array de strings (clave: ingredients)."
                        # "Pasos detallados para preparar la receta (clave: steps)."
                        # "Cantidad de calorias totales (clave: calories)"
                        # "Información nutricional (hidratos de carbono, proteínas, grasas), cada valor como un string en el formato nutrient: value (clave: nutritional_values), donde cada valor debe estar en un string separado dentro de un array."
                        # "Tiempo de preparación (clave: prep_time)."
                        # "Enlace a una imagen representativa, del plato generado anteriormente (clave: image)."
                        # "La respuesta debe estar en formato JSON con las siguientes claves: name, image, description, ingredients, steps, calories, prep_time, y nutritional_values. Los ingredientes deben estar en formato de texto, no como objetos, y los valores nutricionales deben ser un array de strings en lugar de objetos. Además, asegúrate de variar las recetas generadas para que no se repitan."
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

