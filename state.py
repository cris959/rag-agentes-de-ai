from typing import TypedDict, Optional, List

class AgentState(TypedDict):
    pregunta: str
    respuesta: Optional[str]
    rag_exito: bool
    accion_final: str
    historial_nodos: List[str] # Para registrar el camino en la interfaz