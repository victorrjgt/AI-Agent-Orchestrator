from langchain_google_genai import ChatGoogleGenerativeAI
from backend.agents.state import AgentState

# Inicializamos a Gemini. 
# Fíjate que aquí usamos temperature=0.5. Como es el redactor, 
# le damos un poco más de "creatividad" y fluidez para escribir.
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.5)

def writer_node(state: AgentState):
    """
    Este es el nodo del redactor.
    Toma los apuntes del investigador y redacta el artículo/informe final.
    """
    # Leemos el estado
    topic = state["topic"]
    research_data = state["research_data"]  # Aquí están los apuntes del agente anterior
    
    print(f"Escribiendo el informe ejecutivo sobre '{topic}'...")
    
    # Le damos su personalidad y sus reglas estrictas
    prompt = f"""
    Eres un redactor experto y analista corporativo senior. Tu tarea es escribir un informe 
    ejecutivo, claro y profesional sobre el siguiente tema: '{topic}'.
    
    Aquí tienes las notas y datos clave que nuestro equipo de investigación ha recopilado:
    {research_data}
    
    Instrucciones estrictas:
    1. Escribe un informe bien estructurado y directo al grano.
    2. Usa formato Markdown (títulos con ##, listas con viñetas, palabras clave en negrita) para que sea fácil de escanear visualmente.
    3. NO inventes absolutamente nada (cero alucinaciones). Básate estrictamente en los datos de la investigación proporcionada.
    4. Añade una breve conclusión al final.
    """
    
    # Gemini se pone a escribir
    response = llm.invoke(prompt)

    # Extraemos el texto limpio
    contenido = response.content
    texto_limpio = ""
    if isinstance(contenido, str):
        texto_limpio = contenido
    elif isinstance(contenido, list) and len(contenido)>0:
        primer_elemento = contenido[0]
        if isinstance(primer_elemento,dict) and "text" in primer_elemento:
            texto_limpio = primer_elemento["text"]
        else:
            texto_limpio = str(primer_elemento)
    else:
        texto_limpio = str(contenido)
    
    # Guardamos el artículo terminado en la última página de nuestra libreta
    return {"final_report": texto_limpio}