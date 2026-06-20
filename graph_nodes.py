from state import AgentState
from services.llm_service import generar_respuesta_rag

def nodo_triaje(state: AgentState):
    pregunta_input = state["pregunta"].lower()
    historial = state.get("historial_nodos", []) + ["🕵️ Triaje"]
    
    # Clasificación básica por palabras clave
    if any(k in pregunta_input for k in ["reembolso", "comidas", "politica", "gasto", "manual"]):
        return {"accion_final": "rag", "historial_nodos": historial}
    elif any(k in pregunta_input for k in ["excepcion", "teletrabajar", "home office", "remoto"]):
        return {"accion_final": "info", "historial_nodos": historial}
    else:
        return {"accion_final": "ticket", "historial_nodos": historial}

def nodo_auto_resolver(state: AgentState):
    historial = state.get("historial_nodos", []) + ["🤖 Auto Resolver (RAG con Groq)"]
    print(f"🔍 [GRAFO] Nodo auto_resolver activado para: '{state['pregunta']}'")
    
    # El nodo solo llama al servicio, no sabe cómo funciona FAISS ni Groq por dentro
    respuesta, exito = generar_respuesta_rag(state["pregunta"])
    
    return {
        "respuesta": respuesta,
        "rag_exito": exito,
        "historial_nodos": historial
    }

def nodo_pedir_info(state: AgentState):
    historial = state.get("historial_nodos", []) + ["📝 Pedir Información"]
    return {
        "respuesta": "Para procesar excepciones de teletrabajo, por favor indicá las fechas solicitadas en la interfaz.",
        "accion_final": "end",
        "historial_nodos": historial
    }

def nodo_abrir_ticket(state: AgentState):
    historial = state.get("historial_nodos", []) + ["🎫 Abrir Ticket"]
    return {
        "respuesta": "No encontré políticas internas que respondan a tu consulta en nuestros documentos. He derivado un ticket automático a un agente humano de RR.HH.",
        "historial_nodos": historial
    }

# --- ARISTAS CONDICIONALES (Se mantienen intactas y limpias) ---
def arista_decision_triaje(state: AgentState): return state["accion_final"]
def arista_resultado_rag(state: AgentState): return "ok" if state["rag_exito"] else "ticket"
def arista_resultado_info(state: AgentState): return state["accion_final"]