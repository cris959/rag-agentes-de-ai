import gradio as gr
from workflow import agente_app

def procesar_consulta(pregunta_usuario):
    # Inicializamos el estado del grafo
    inputs = {"pregunta": pregunta_usuario, "historial_nodos": []}
    
    # Ejecutamos el agente de forma síncrona para congelar el resultado final
    resultado = agente_app.invoke(inputs)
    
    # Extraemos los datos que nos interesan mostrar
    respuesta_final = resultado.get("respuesta", "Sin respuesta.")
    camino_seguido = " ➔ ".join(resultado.get("historial_nodos", []))
    
    return respuesta_final, camino_seguido

# --- DISEÑO DE LA INTERFAZ CON GRADIO ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏆 Sistema de Agentes RR.HH. - 'La Escaloneta'")
    gr.Markdown("Ingresá tu consulta para ver cómo el Grafo de Estados rutea y resuelve tu caso usando Groq.")
    
    with gr.Row():
        with gr.Column():
            input_texto = gr.Textbox(label="Consulta del Empleado", placeholder="Ej: ¿Puedo pedir reembolso de internet?")
            boton_enviar = gr.Button("Disparar Agente", variant="primary")
            
        with gr.Column():
            output_respuesta = gr.Textbox(label="🤖 Respuesta del Agente", interactive=False)
            output_camino = gr.Label(label="📍 Ruta de Nodos Activados en Tiempo Real")

    # Acción del botón
    boton_enviar.click(
        fn=procesar_consulta,
        inputs=input_texto,
        outputs=[output_respuesta, output_camino]
    )

# Lanzamos el servidor local
if __name__ == "__main__":
    demo.launch()