import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="Chatbot con IA", page_icon="💬", layout="centered")

# Cargar la API key de forma segura
try:
    load_dotenv()  # Carga variables desde .env si existe (entorno local)
    API_KEY = os.getenv("GROQ_API_KEY")  #para Groq; usar "OPENAI_API_KEY" si es OpenAI
except:
    API_KEY = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = API_KEY
client = Groq()  # Cliente para invocar la API de Groq

# Inicializar el historial de chat en la sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # lista de dicts: {"role": ..., "content": ...}

SYSTEM_PROMPT = """Eres un asistente virtual amable y experto en cardiología, además eres un experto en venta. Vas a contestar preguntas relacionado sobre un wearable 
llamado cardio core encardo de ekg y vas a ayudarnos en lo que es la venta de este producto, este producto puede ser o alguilado 14 días o puede ser comprado para uso permanente
Los precios de alquiler es 100 soles y el de venta en precio unitario es S/ 900 por unidad, aparte hay un plan mensual que te ayuda a guardar más datos y exportarlo.
Lo innovador de cardiocore es que a diferencia de un holter te acompaña siempre, no solo 1 día o no, es portable y comodo para el uso diario y las exportanciones de lo monitoreado en el ekg son instantaneas"""

st.title(" ❤️ Cardio core chatbot ❤️")
st.write("Cardiocore siempre presente para ti")
st.write("Puedes hacer preguntas y el chatbot responderá usando un modelo de lenguaje.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes para el modelo
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.extend(st.session_state.chat_history)

    # Llamar a la API **solo** si hay user_input (evita NameError)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )
        respuesta_texto = response.choices[0].message.content  # objeto, no dict
    except Exception as e:
        respuesta_texto = f"Lo siento, ocurrió un error al llamar a la API: `{e}`"

    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

    # Guardar en historial
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})
