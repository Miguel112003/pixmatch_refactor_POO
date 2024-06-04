# Punto de entrada de la aplicación
import streamlit as st

from controllers.gui_controller import GUIController

# Set page title, icon, layout wide (more used space in central area) and sidebar initial state
st.set_page_config(page_title="PixMatch_OOP", page_icon="🕹️", layout="wide",
                   initial_sidebar_state="expanded")
if __name__ == "__main__":
    # Punto de entrada de la aplicación, llama al controlador de la interfaz gráfica
    gui = GUIController()
    gui.main()
