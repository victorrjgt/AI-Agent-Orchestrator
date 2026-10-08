import streamlit as st
import requests

# 1. Configuración visual de la página
st.set_page_config(page_title="Investigador IA", page_icon="🕵️‍♂️", layout="centered")

st.title("Equipo de Investigación Autónomo")
st.write("Escribe un tema. Nuestro agente investigador buscará en la web y el agente redactor escribirá el informe final.")

# 2. Caja de texto para que el usuario pida el tema
tema = st.text_input("¿Qué quieres investigar hoy?", placeholder="Ej: Impacto de la Inteligencia Artificial en la educación")

# 3. El botón que desencadena la acción
if st.button("Iniciar Investigación", type="primary"):
    if not tema:
        st.warning("Por favor, escribe un tema primero.")
    else:
        # Mostramos un spinner bonito mientras esperamos al backend
        with st.spinner(f"Los agentes están trabajando en: '{tema}'. Esto tomará unos segundos..."):
            try:
                # Hacemos la petición a FastAPI
                # Le enviamos el tema en formato JSON tal como nos pedía el AgentState
                respuesta = requests.post(
                    "http://127.0.0.1:8000/api/investigar",
                    json={"topic": tema}
                )
                
                # Si FastAPI nos devuelve el informe con éxito (código 200)
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    st.success("¡Investigación completada!")
                    
                    # CAJA DE COLOR PARA EL INFORME
                    with st.container(border=True):
                        st.info(f"**Tema investigado:** {datos['tema']}")
                        # Imprimimos el informe final limpio
                        st.markdown(datos["informe"])
                        
                    # BIBLIOGRAFÍA DESPLEGABLE
                    with st.expander("Ver Bibliografía y Fuentes Consultadas"):
                        st.write("La información de este informe ha sido extraída de las siguientes fuentes en tiempo real:")
                        # Recorremos la lista de enlaces y los mostramos de forma segura
                        for url in datos.get("fuentes", []):
                            st.markdown(f"- [{url}]({url})")
                else:
                    st.error(f"El servidor reportó un error: {respuesta.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 No se pudo conectar con el servidor. ¿Seguro que FastAPI está encendido en la otra terminal?")