import os
from dotenv import load_dotenv

# Esto lee tu archivo .env oculto
load_dotenv()

# Guardamos las variables para usarlas luego
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Aviso en caso de que no tenga las claves
if not GOOGLE_API_KEY or not TAVILY_API_KEY:
    raise ValueError("Faltan las API Keys en el .env")