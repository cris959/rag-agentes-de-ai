import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Cargamos el archivo .env
load_dotenv()

# Instanciamos el modelo de Groq (usando Llama 3.3 de 70B que es un cañón)
llm = ChatGroq(
    temperature=0.3,
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)