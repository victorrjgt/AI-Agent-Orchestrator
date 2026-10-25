from typing import TypedDict
from langgraph.graph import StateGraph, END
from backend.agents.state import AgentState
from backend.agents.researcher import research_node
from backend.agents.writer import writer_node


# Importamos a nuestros dos nodos
from backend.agents.researcher import research_node
from backend.agents.writer import writer_node

# Creamos el tablero de trabajo (Graph) indicando qué libreta vamos a usar
workflow = StateGraph(AgentState)

# Contratamos a los trabajadores (Añadimos los Nodos)
# Al nodo le ponemos un nombre interno ("investigador") y le asignamos su función
workflow.add_node("investigador", research_node)
workflow.add_node("redactor", writer_node)

# Diseñamos la cadena de montaje (Añadimos los Edges/Bordes)
# - El proceso empieza siempre por el investigador
workflow.set_entry_point("investigador")

# - Cuando el investigador termina, le pasa la libreta al redactor
workflow.add_edge("investigador", "redactor")

# - Cuando el redactor termina, el proceso finaliza (END)
workflow.add_edge("redactor", END)

# - Compilamos (ensamblamos) el motor final
orquestador = workflow.compile()
