from typing import TypedDict

class AgentState(TypedDict):
    topic: str
    research_data: str
    final_report: str
    sources: list[str] # Lista de las URL