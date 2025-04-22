"""Módulo que permite enviar consultas a la API de ChatGPT y recuperar respuestas en consola."""

import openai  # importa la biblioteca openai para interactuar con la API

# Establecer la clave API de OpenAI
openai.api_key = "sk-proj-..."

# Contexto y tarea para el modelo GPT
CONTEXT = "Sos un asistente de inteligencia artificial que responde preguntas clara y útilmente."
USER_TASK = "El usuario va a hacer una consulta y vos tenés que responderla."

def consultar_chatgpt(mensaje):
    """Llama a la API de OpenAI y devuelve la respuesta."""
    response = openai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",  # Modelo que se usará para generar la respuesta
        messages=[  # Se pasa el contexto, la tarea y la consulta del usuario
            {"role": "system", "content": CONTEXT},
            {"role": "user", "content": USER_TASK},
            {"role": "user", "content": mensaje}
        ],
        temperature=1,
        max_tokens=16384,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

def main():
    """Función principal que gestiona la interacción con el usuario y la API."""
    import readline  # importa readline para manejar la entrada de texto y permitir el historial

    # Número máximo de entradas en el historial
    readline.set_history_length(10)

    while True:
        try:
            # Solicita la consulta del usuario, con opción de usar la última consulta
            user_query = input("Ingrese su consulta (o 'Enter' para última consulta): ").strip()

            # Si la consulta está vacía, se recupera la última consulta del historial
            if not user_query:
                if readline.get_current_history_length() > 0:
                    user_query = readline.get_history_item(readline.get_current_history_length())
                    print(f"Recuperando última consulta: {user_query}")
                else:
                    print("No hay consultas previas para recuperar.")  # Mensaje si no hay historial
                    continue  # Vuelve a pedir una consulta

            # Si la consulta sigue vacía, se termina la ejecución
            if not user_query:
                print("Consulta vacía.")
                return

            # Agrega la nueva consulta al historial
            readline.add_history(user_query)

            # Imprime la consulta introducida por el usuario
            print("You:", user_query)

            # Llama a la API para obtener la respuesta
            respuesta = consultar_chatgpt(user_query)

            # Imprime la respuesta generada por GPT
            print("chatGPT:", respuesta)

        except openai.OpenAIError as api_error:
            print(f"Error con la API: {api_error}")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")

        # Opción de salir del programa
        if user_query.lower() in ("salir", "exit"):
            print("Programa finalizado.")
            break

if __name__ == "__main__":
    main()
