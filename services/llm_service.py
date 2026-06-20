from config import llm
from services.database import retriever
from langchain_core.prompts import ChatPromptTemplate

def generar_respuesta_rag(pregunta: str) -> tuple[str | None, bool]:
    """
    Busca contexto en los PDFs y genera una respuesta usando Groq.
    Retorna: (texto_respuesta, exito_rag)
    """
    # 1. Recuperamos fragmentos de los PDFs
    docs_relevantes = retriever.invoke(pregunta)
    contexto = "\n\n".join([doc.page_content for doc in docs_relevantes])
    
    # Si la base de datos no tiene contenido relevante, abortamos con éxito falso
    if not contexto.strip():
        return None, False
        
    # 2. Diseñamos el prompt estructurado
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Sos el asistente experto en RR.HH. de 'La Escaloneta'. "
            "Respondé la consulta del empleado de forma clara y concisa basándote ÚNICAMENTE "
            "en el siguiente contexto extraído de los manuales de la empresa. "
            "Si la respuesta no figura explícitamente en el contexto, devolvé la palabra clave: [SIN_DATOS]\n\n"
            "Contexto:\n{contexto}"
        )),
        ("human", "{pregunta}")
    ])
    
    # 3. Inferencia con Llama 3.3 en Groq
    cadena = prompt | llm
    respuesta_llm = cadena.invoke({"contexto": contexto, "pregunta": pregunta})
    contenido = respuesta_llm.content.strip()
    
    # Validamos si el LLM detectó que no tiene info
    if "[SIN_DATOS]" in contenido or len(contenido) < 5:
        return None, False
        
    return contenido, True