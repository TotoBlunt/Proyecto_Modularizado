import streamlit as st
import importlib
import sys
import os
from proyectos.Proyecto2.FrontEnd.estilos_st import aplicar_estilos
from scripts.integrantes import mostrar_integrantes

sys.path.append(os.path.join(os.path.dirname(__file__), "private"))

# Guardar selección en sesión para evitar reinicios
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
        modulo.ejecutar(st.session_state.data_source, st.session_state.uploaded_file)
    else:
        st.error(f"No se pudo cargar la versión {version}")

# Interfaz principal
def main():
    st.title("Selector de Versiones")

    # Paso 1: Seleccionar versión antes de continuar
    version_seleccionada = st.selectbox(
        "Selecciona la versión que deseas ejecutar:",
        options=["Proyecto2"],  # Eliminamos Proyecto1 si está vacío
        index=0
    )

    if st.button("Confirmar Versión"):
        st.session_state.selected_version = version_seleccionada

    # No avanzar hasta que se confirme la versión
    if st.session_state.selected_version:
        st.success(f"Versión seleccionada: {st.session_state.selected_version}")

        # Paso 2: Elegir la fuente de datos
        st.session_state.data_source = st.radio(
            "¿Desde dónde quieres cargar el modelo?",
            ["Supabase", "CSV/Excel"]
        )

        # Si el usuario elige CSV/Excel, subir archivo
        if st.session_state.data_source == "CSV/Excel":
            st.session_state.uploaded_file = st.file_uploader("Carga tu archivo", type=["csv", "xlsx"])

        # Paso 3: Ejecutar versión cuando todo está listo
        if st.button("Ejecutar Versión") and st.session_state.data_source:
            ejecutar_version(st.session_state.selected_version)

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    aplicar_estilos()

    col1, col2 = st.columns([2, 8])

    with col1:
        mostrar_integrantes()

    with col2:
        main()
