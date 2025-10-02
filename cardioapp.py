import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="Chatbot con IA", page_icon="💬", layout="centered")

# Agregar al inicio del script, después de st.set_page_config
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        color: #e63946 !important;
        text-align: center;
        margin-bottom: 1rem;
    }
    .cardio-subtitle {
        font-size: 1.2rem;
        color: #457b9d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .user-message {
        background-color: #f1faee;
        padding: 12px;
        border-radius: 10px;
        border-left: 4px solid #e63946;
    }
    .assistant-message {
        background-color: #a8dadc;
        padding: 12px;
        border-radius: 10px;
        border-left: 4px solid #1d3557;
    }
    .price-highlight {
        background-color: #ffd166;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: bold;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

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

SYSTEM_PROMPT = """Eres CardioCore Assistant, un especialista en cardiología y ventas con experiencia en wearables médicos. 
Tu enfoque principal es el dispositivo CardioCore, un monitor cardíaco portátil de ECG.

**INFORMACIÓN DEL PRODUCTO:**
- **Dispositivo:** CardioCore - Monitor ECG portátil
- **Opción Alquiler:** 14 días por S/ 100 (ideal para evaluación)
- **Opción Compra:** S/ 900 por unidad (uso permanente)
- **Plan Mensual Premium:** Almacenamiento extendido y exportaciones avanzadas
- **Ventajas clave:** Portátil, monitoreo continuo (no limitado a 24h), cómodo para uso diario, exportaciones instantáneas
- **Contacto:** cardiocore@gmail.com (solo Lima)

**DIRECTIVAS DE COMUNICACIÓN:**
1. Sé empático, profesional y entusiasta sobre la salud cardíaca
2. Destaca las ventajas vs. holters tradicionales
3. Cuando mencionen precios, usa formato claro: "S/ 900" o "S/ 100"
4. Ofrece el contacto email naturalmente cuando haya interés de compra
5. Explica beneficios en términos de salud y conveniencia

**RESPONDE EN ESPAÑOL** y mantén un tono cálido pero profesional."""

st.title(" ❤️ Cardio core chatbot ❤️")
st.write("Cardiocore siempre presente para ti")
st.write("Puedes hacer preguntas y el chatbot responderá usando un modelo de lenguaje.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("💬 Escribe tu pregunta sobre CardioCore")

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

st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.markdown("**❤️ CardioCore**")
    st.markdown("Tu salud cardíaca, nuestra prioridad")

with footer_col3:
    st.markdown("**📞 Soporte**")
    st.markdown("cardiocore@gmail.com")
