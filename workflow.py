from langgraph.graph import START, END, StateGraph
from state import AgentState
from graph_nodes import (
    nodo_triaje, nodo_auto_resolver, nodo_pedir_info, nodo_abrir_ticket,
    arista_decision_triaje, arista_resultado_rag, arista_resultado_info
)

def construir_agente():
    workflow = StateGraph(AgentState)
    
    # Agregar Nodos
    workflow.add_node("triaje", nodo_triaje)
    workflow.add_node("auto_resolver", nodo_auto_resolver)
    workflow.add_node("pedir_info", nodo_pedir_info)
    workflow.add_node("abrir_ticket", nodo_abrir_ticket)
    
    # Configurar Conexiones
    workflow.add_edge(START, "triaje")
    
    workflow.add_conditional_edges(
        "triaje", 
        arista_decision_triaje, 
        {"rag": "auto_resolver", "ticket": "abrir_ticket", "info": "pedir_info"}
    )
    workflow.add_conditional_edges(
        "auto_resolver", 
        arista_resultado_rag, 
        {"ok": END, "ticket": "abrir_ticket", "info": "pedir_info"}
    )
    workflow.add_conditional_edges(
        "pedir_info", 
        arista_resultado_info, 
        {"ticket": "abrir_ticket", "end": END}
    )
    
    workflow.add_edge("abrir_ticket", END)
    
    return workflow.compile()

# Instancia global del grafo compilado listo para usar
agente_app = construir_agente()