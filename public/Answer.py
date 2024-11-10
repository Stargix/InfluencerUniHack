from flask import Flask, request, jsonify
from groq import Groq
import groq
from dotenv import load_dotenv
import os
import flask

load_dotenv()
api_key = os.getenv("LLAMA_API_KEY")

client = Groq(
    api_key=api_key,
)
# Inicializa el historial de mensajes como una lista vacía

def obtener_respuesta(mensaje_usuario):
    # Crea la llamada a la API con el historial completo de mensajes
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an Instagram user. You are answering a message from a potential business client. Respond in a professional manner. But don't accept any business offers."}
        ],
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0.5,
        max_tokens=1024,
        stop=None,
        stream=False,
    )

    # Añade la respuesta del asistente al historial
    respuesta = chat_completion.choices[0].message.content
    # No se añade la respuesta al historial ya que se ha quitado el historial

    app = Flask(__name__)

    @app.route('/answer', methods=['POST'])
    def answer():
        data = request.json
        message = data.get('message', 'No message received')
        response = {'message': f'Received: {message}'}
        return jsonify(response)

    if __name__ == '__main__':
        app.run(debug=True, port=8080)