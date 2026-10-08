from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.agents.graph import orquestador
from backend.agents.state import AgentState

# Creamos la aplicación
app = FastAPI(
    title="API de Investigación Autónoma",
    description="Sistema Multi-Agente con LangGraph y Gemini"
)

# Definimos el contrato de validación
# Pydantic asegura que nadie pueda pedir algo incorrecto. 
# Obliga a que la petición traiga siempre un campo llamado "topic" que sea texto.
class ResearchRequest(BaseModel):
    topic: str

# Creamos el Endpoint (La puerta de entrada)
@app.post("/api/investigar")
async def investigar_tema(request: ResearchRequest):
    print(f"Petición recibida en la API. Tema: {request.topic}")
    
    try:
        # Preparamos la primera página de la "libreta" con el tema pedido
        estado_inicial = AgentState(
                topic=request.topic,
                research_data="",
                final_report="",
                sources=[]
            )
        
        # Damos la orden al Orquestador
        # .invoke() hace que arranque todo el proceso: Investigador -> Redactor -> Fin
        resultado_final = orquestador.invoke(estado_inicial)
        
        # Devolvemos únicamente el informe final al usuario
        return {
            "tema": request.topic,
            "informe": resultado_final["final_report"],
            "fuentes": resultado_final["sources"]
        }
        
    except Exception as e:
        # Si algo falla le damos un error claro al cliente
        print(f"Error en la API: {e}")
        raise HTTPException(status_code=500, detail=str(e))