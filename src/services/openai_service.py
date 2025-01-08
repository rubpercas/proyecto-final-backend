import os
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la clave API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_recipe_with_ai(prompt):
    """
    Genera una receta usando la API de OpenAI.
    :param prompt: Texto descriptivo de la receta.
    :return: Respuesta generada por OpenAI.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Puedes usar "gpt-3.5-turbo" si no tienes acceso a GPT-4
            messages=[
                {"role": "system", "content": "Eres un asistente culinario experto en crear recetas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error al generar receta con OpenAI: {e}")
        return None
