from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from backend.core.config import TAVILY_API_KEY
from backend.agents.state import AgentState

# Inicializamos las herramientas
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Usamos gemini-1.5-flash porque rápido y barato/gratis
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)

def research_node(state: AgentState):
    """
    Este es el nodo del investigador.
    Recibe el tema, busca en Google y le pide a Gemini que lo resuma.
    """
    topic = state["topic"]
    print(f"Buscando en internet sobre '{topic}'...")
    
    # Buscar en internet los 3 mejores resultados recientes (Podemos modificar basic por advanced pero consume más)
    # podemos modificar el número de resultados max_results a más de 3
    # La query es lo que vamos a buscar que es el topic que el usuario ingresa
    search_result = tavily_client.search(query=topic, search_depth="basic", max_results=3)

    # URL
    enlaces = [r["url"] for r in search_result["results"]]
    
    # Extraemos solo el texto útil de las páginas web
    # Se extrae el texto de las 3 páginas web y se genera una lista de Python con los textos
    #  \n\n.join lo que hace es pegar todos los textos en un solo párrafo poniendo saltos de líneas entre web
    context = "\n\n".join([r["content"] for r in search_result["results"]])
    
    # Gemini lee los textos brutos y saca lo importante
    print("Analizando y resumiendo los datos leídos...")
    prompt = f"""
    Eres un investigador analítico. Tu objetivo es extraer la información más relevante 
    sobre este tema: '{topic}'.
    
    Aquí tienes la información en bruto sacada de internet:
    {context}
    
    Escribe un resumen con los puntos clave, datos duros y fechas importantes.
    """
    
    response = llm.invoke(prompt)

    contenido = response.content
    texto_limpio = ""
    if isinstance(contenido, str):
        texto_limpio = contenido
    elif isinstance(contenido, list) and len(contenido) > 0:
        primer_elemento = contenido[0]
        if isinstance(primer_elemento, dict) and "text" in primer_elemento:
            texto_limpio = primer_elemento["text"]
        else:
            texto_limpio = str(primer_elemento)
    else:
        texto_limpio = str(contenido)
    
    # Guardamos los apuntes limpios en el estado
    return {"research_data": texto_limpio, "sources": enlaces}
