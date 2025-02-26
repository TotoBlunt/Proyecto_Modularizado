import streamlit as st
import importlib
import sys
import os
from proyectos.Proyecto2.FrontEnd.estilos_st import aplicar_estilos
from scripts.integrantes import mostrar_integrantes

sys.path.append(os.path.join(os.path.dirname(__file__), "private"))

# Inicializar el estado de la sesión
if "selected_version" not in st.session_state:
    st.session_state.selected_version = None

if "data_source" not in st.session_state:
    st.session_state.data_source = None

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

def cargar_version(version):
    try:
        modulo = importlib.import_module(f"proyectos.{version}.principal")
        return modulo
    except ImportError as e:
        st.error(f"Error al cargar la versión {version}: {e}")
        return None

def ejecutar_version(version):
    modulo = cargar_version(version)
    if modulo:
        st.success(f"Ejecutando {version}...")
        # Llamar a la función ejecutar sin parámetros
        modulo.ejecutar()  # Aquí no se pasan parámetros
    else:
        st.error(f"No se pudo cargar la versión {version}")

# Interfaz principal
def main():

    st.title("Proyecto Productivo para la predicción del peso de pollos usando variables descritas por el modelo SelectKBest, luego hacer las predicciones usando el Modelo Ensemble, con Streamlit")
    
    st.title("Selector de Versiones")

    # Paso 1: Seleccionar versión
    version_seleccionada = st.selectbox(
        "Selecciona la versión que deseas ejecutar:",
        options=["Proyecto1", "Proyecto2"],  
        index=0 if st.session_state.selected_version is None else ["Proyecto1", "Proyecto2"].index(st.session_state.selected_version)
    )

    # Actualizar el estado de la versión seleccionada
    st.session_state.selected_version = version_seleccionada

    if st.session_state.selected_version:
        st.success(f"Versión seleccionada: {st.session_state.selected_version}")

        ejecutar_version(st.session_state.selected_version)

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    aplicar_estilos()

    col1, col2 = st.columns([2, 8])

    with col1:
        mostrar_integrantes()

    with col2:
        main()