"""
Chatbot Básico usando Python + ChatGPT
"""

# Importar bibliotecas y configurar clave
import os
import openai
import spacy
import numpy as np
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Variables
preguntas_anteriores = []
respuestas_anteriores = []
modelo_spacy = spacy.load("es_core_news_md")
# La siguiente linea es la lista negra de palabras a censurar, modificar a conveniencia
palabras_prohibidas = ["palabra1", "palabra2"]

# Función para la Similitud de los Vectores
def similitud_coseno(vec1, vec2):
    """Función para la Similitud de los vectores"""
    superposicion = np.dot(vec1, vec2)
    magnitud1 = np.linalg.norm(vec1)
    magnitud2 = np.linalg.norm(vec2)
    sim_cos = superposicion / (magnitud1 * magnitud2)
    return sim_cos

# Cálculo entre dos valores de texto
def es_relevante(respuesta, entrada, umbral=0.25):
    """Cálculo entre dos valores de texto"""
    entrada_vectorizada = modelo_spacy(entrada).vector
    respuesta_vectorizada = modelo_spacy(respuesta).vector
    similitud = similitud_coseno(entrada_vectorizada, respuesta_vectorizada)
    return similitud >= umbral

# Función para filtrar lista negra de palabras
def filtrar_lista_negra(texto, lista__negra):
    """Función para filtrar lista negra de palabras"""
    tokens = modelo_spacy(texto)
    resultado = []

    for token in tokens:
        if token.text.lower() not in lista__negra:
            resultado.append(token.text)
        else:
            resultado.append("[XXXXX]")
    return " ".join(resultado)

# Función para peticiones
def preguntar_chat_gpt(prompt, modelo="text-davinci-002"):
    """Función para peticiones"""
    respuesta = openai.Completion.create(
        engine=modelo,
        prompt=prompt,
        n=1,
        max_tokens=150,
        temperature=1.5
    )
    respuesta_sin_control =  respuesta.choices[0].text.strip()
    respuesta_controlada = filtrar_lista_negra(respuesta_sin_control, palabras_prohibidas)
    return respuesta_controlada

# Funcionamiento básico
os.system("clear" or "cls")
print("-----------------------------------------------------------------------")
print("                   Bienvenido al Chatbox del El Neto                   ")
print("               Escribe 'salir' cuando quieras terminar...              ")
print("-----------------------------------------------------------------------")

while True:
    CONVERSACION_HISTORICA = ""
    ingreso_usuario = input("\nTú: ")
    if ingreso_usuario.lower() == "salir":
        print("\nGracias por platicar con nuestro Chatbot Básico, que tengas un excelente día...\n")
        break

    for pregunta, resp in zip(preguntas_anteriores, respuestas_anteriores):
        CONVERSACION_HISTORICA += f"El usuario pregunta: {pregunta}\n"
        CONVERSACION_HISTORICA += f"ChatGPT responde: {resp}\n"

    prompt = f"El usuario pregunta: {ingreso_usuario}\n:"
    CONVERSACION_HISTORICA += prompt
    RESPUESTA_GPT = preguntar_chat_gpt(CONVERSACION_HISTORICA)

    relevante = es_relevante(RESPUESTA_GPT, ingreso_usuario)

    if relevante:
        print("\n")
        print(f"Chatbox: {RESPUESTA_GPT}")
        # Almacenar las conversaciones
        preguntas_anteriores.append(ingreso_usuario)
        respuestas_anteriores.append(RESPUESTA_GPT)
    else:
        print("\n")
        print("La respuesta no es relevante")
