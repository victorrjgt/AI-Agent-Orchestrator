# Investigador IA Multi-Agente

Este proyecto es un orquestador de IA basado en LangGraph, FastAPI y Streamlit. Utiliza un sistema multi-agente donde un **Agente Investigador** busca información en tiempo real (vía Tavily) y un **Agente Redactor** (Gemini) sintetiza los datos en un informe ejecutivo en formato Markdown.

## Tecnologías utilizadas
* **LangGraph & LangChain:** Orquestación de agentes y manejo del LLM.
* **Google Gemini (2.5-flash):** Motor de razonamiento y redacción.
* **Tavily Search API:** Búsqueda optimizada para agentes de IA.
* **FastAPI:** Backend que expone el orquestador mediante una API REST.
* **Streamlit:** Interfaz de usuario interactiva y amigable.

## Cómo ejecutar el proyecto en local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/victorrjgt/Orquestador.git
cd Orquestador
```
2. **Crear entorno virtual e instalar dependencias:**
```bash
python -m venv .venv
# Activar entorno (Windows): ..venv\Scripts\Activate.ps1
# Activar entorno (Mac/Linux): source .venv/bin/activate
pip install uv
uv pip install -r backend/requirements.txt
```

3. **Configurar variables de entorno:**
* Renombra el archivo `.env.example` a `.env`.
* Introduce tus propias API Keys de Google AI Studio y Tavily.

4. **Arrancar el servidor (Backend):**
```bash
uvicorn backend.api.server:app --reload
```

5. **Arrancar la interfaz (Frontend) en una nueva terminal:**
```bash
streamlit run frontend/app.py
```
