# 🏆 RR.HH. AI Agent - "La Escaloneta" 

Este proyecto consiste en el desarrollo de un **Agente Cognitivo Avanzado** orientado a la gestión y automatización de consultas de Recursos Humanos para la empresa simulada *"La Escaloneta Desarrollo de Software"*. 

A diferencia de los pipelines lineales tradicionales, este sistema rompe el paradigma utilizando una **arquitectura de grafos de estado cíclicos**, lo que permite al agente tomar decisiones dinámicas, iterar con el usuario y derivar casos de forma inteligente en tiempo real.

## 📐 Arquitectura del Flujo (Diseño del Grafo)

El agente utiliza **LangGraph** para estructurar el ciclo de vida de una consulta mediante nodos (estaciones de trabajo) y aristas condicionales (inspectores de tráfico basados en el estado):
___
````mermaid
graph TD
    %% Definición de Estilos
    classDef startEnd fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff;
    classDef nodeStyle fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff;
    classDef routerStyle fill:#f1c40f,stroke:#f39c12,stroke-width:2px,color:#333;

    %% Nodos Principales
    START((🚀 START))
    END((🛑 END))
    NodoTriaje[🕵️ Nodo: triaje]
    AristaDecision{¿Qué camino<br>tomar?}
    
    NodoRAG[🤖 Nodo: auto_resolver]
    NodoInfo[📝 Nodo: pedir_info]
    NodoTicket[🎫 Nodo: abrir_ticket]

    %% Conexiones (Flujo)
    START --> NodoTriaje
    NodoTriaje --> AristaDecision
    
    AristaDecision -- "rag" --> NodoRAG
    AristaDecision -- "info" --> NodoInfo
    AristaDecision -- "ticket" --> NodoTicket
    
    NodoRAG -- "ok" --> END
    NodoRAG -- "ticket" --> NodoTicket
    NodoRAG -- "info" --> NodoInfo
    
    NodoInfo -- "end" --> END
    NodoInfo -- "ticket" --> NodoTicket
    
    NodoTicket --> END

    %% Aplicación de Estilos
    class START,END startEnd;
    class NodoTriaje,NodoRAG,NodoInfo,NodoTicket nodeStyle;
    class AristaDecision routerStyle;


````
___

🔁 Lógica de los Nodos

* **triaje**: Analiza la consulta inicial del empleado y clasifica la intención dentro del **AgentState**.

* **auto_resolver** (RAG Component): Ejecuta la búsqueda de embeddings en la base vectorial (FAISS) y responde usando el LLM (Llama 3.3 via Groq). Si la respuesta es concluyente, finaliza (**ok -> END**). Si falla o es ambigua, se redirige dinámicamente a soporte o solicitud de información.

* **pedir_info**: Se activa si faltan parámetros clave (ej. fechas para una excepción de teletrabajo).

* **abrir_ticket**: El nodo de escape. Si la consulta está fuera de contexto (ej. preguntas del Mundial) o el RAG no tiene datos, genera un ticket automático en la mesa de ayuda humana.

## 🛠️ Tecnologías y Herramientas Utilizadas
1- Orquestación de Agentes: LangGraph (**StateGraph, START, END**).

2- Lógica y Esquemas: Python 3.10+ & **TypedDict** para la gestión estricta de la memoria del estado (**AgentState**).

3- LLM / Inferencia: Llama 3.3 (70B) optimizado mediante la API de Groq Cloud.

4- Ecosistema RAG: LangChain (LCEL), Embeddings de HuggingFace, y Vector Store FAISS.

5- Monitoreo: Ejecución por pasos mediante **app.stream(..., stream_mode="updates"**) para trazabilidad total en consola.

6- Entorno de Desarrollo: Google Colab.

## 💻 Ejemplo de Ejecución (Streaming de Estados)
El repositorio incluye un script de prueba que procesa en lote (iteración) diferentes tipos de consultas de empleados, mostrando en consola el ruteo dinámico:

````Plaintext
==================== 📥 CASO #1 ====================
PREGUNTA: 'Quiero una excepcion para teletrabajar durante 5 dias'

 📍 Activado: 'triaje'
    ↳ Decision: Enviar a solicitud de datos adicionales.
 📍 Activado: 'pedir_info'
    ↳ 💬 Respuesta emitida: Por favor indícanos las fechas exactas del pedido.
======================================================
````

## 🚀 Cómo Ejecutar el Cuaderno
1- Cloná este repositorio.

2- Abrí el archivo **.ipynb** en Google Colab.

3- Asegurate de cargar tu **GROQ_API_KEY** en la sección de Secretos de Colab (icono de llave 🔑) para resguardar la seguridad de la credencial.

4- Ejecutá las celdas en orden secuencial para compilar el grafo y lanzar la simulación.
___

# 🤖 Agente de Inteligencia Artificial para RR.HH. - "La Escaloneta"

Este proyecto consiste en un agente inteligente de Recursos Humanos desarrollado con una arquitectura modular y escalable. Utiliza **LangGraph** para la gestión del flujo y toma de decisiones (Grafo de Conocimiento), **FAISS** como base de datos vectorial local para el procesamiento de documentos (RAG), y **Groq (Llama 3.3)** como motor de inferencia de lenguaje.

La interfaz gráfica está montada sobre **Gradio**, permitiendo interactuar con el agente en tiempo real.

---

## 📸 Vista Previa de la Aplicación
![Interfaz de Usuario de La Escaloneta](/multimedia/screenshot_gradio.png)

---

## 🏗️ Arquitectura del Proyecto

El software fue refactorizado desde un entorno lineal (Google Colab) hacia una arquitectura limpia y desacoplada basada en capas de servicios:

* **`services/database.py`**: Gestión de infraestructura vectorial. Descarga el modelo de embeddings `bge-small-en-v1.5`, procesa la carpeta de PDFs locales, fragmenta el texto y persiste el índice FAISS en disco.
* **`services/llm_service.py`**: Encapsula las directrices corporativas (Prompts) y la comunicación con la API de Groq.
* **`graph_nodes.py`**: Lógica de control pura del agente. Lee los estados y delega las tareas a los servicios sin acoplar infraestructura.
* **`app.py`**: Capa de presentación que levanta el servidor web local con Gradio.

---

## 🛠️ Requisitos e Instalación

### 1. Clonar el repositorio e instalar dependencias
```bash
git clone [https://github.com/cris959/rag-agentes-de-ai.git](https://github.com/cris959/rag-agentes-de-ai.git)
cd rag-agentes-de-ai
pip install langchain-graph langchain-huggingface langchain-community faiss-cpu sentence-transformers pypdf gradio python-dotenv
```
2. Configurar Variables de Entorno
Creá un archivo **.env** en la raíz del proyecto (este archivo está protegido por **.gitignore**):

```Plaintext
GROQ_API_KEY=tu_api_key_aqui
```
3. Cargar Documentación Interna
Colocá los archivos PDF con las políticas de la empresa dentro de la carpeta **/documentos**. El sistema los indexará automáticamente en la primera ejecución.

4. Correr la Aplicación
```Bash
python app.py
```
___
## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo [LICENSE](https://github.com/cris959/rag-agentes-de-ai/blob/main/LICENSE) adjunto en este repositorio.

Copyright © 2026 [Christian Garay](https://github.com//cris959/rag-agentes-de-ai) - Backend Developer.
