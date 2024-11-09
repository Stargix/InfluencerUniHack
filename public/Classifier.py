from groq import Groq
import groq

# Inicializa el historial de mensajes como una lista vacía
historial_mensajes = []

# Inicializa el cliente de Groq
client = Groq(
    api_key="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",
)

def obtener_respuesta(mensaje_usuario):
    # Añade el mensaje del usuario al historial
    historial_mensajes.append({
        "role": "user",
        "content": mensaje_usuario,
    })

    # Crea la llamada a la API con el historial completo de mensajes
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a message classifier that can only classify between [family,friends,buisness,other]. Return only one word"}
        ] + historial_mensajes,
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0.5,
        max_tokens=1024,
        stop=None,
        stream=False,
    )

    # Añade la respuesta del asistente al historial
    respuesta = chat_completion.choices[0].message.content
    historial_mensajes.append({
        "role": "assistant",
        "content": respuesta,
    })

    return respuesta

if __name__ == "__main__":
    while True:
        mensaje_usuario = input("Message: ")
        if mensaje_usuario.lower() in ["salir", "exit", "quit"]:
            print("Adiós!")
            break
        respuesta = obtener_respuesta(mensaje_usuario)
        print(f"Answer: {respuesta}")

