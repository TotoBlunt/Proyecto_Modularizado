import streamlit as st
import importlib
import sys
import os
import pandas as pd
from proyectos.Proyecto2.FrontEnd.estilos_st import aplicar_estilos
from scripts.integrantes import mostrar_integrantes

# Agrega la carpeta "private" al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "private"))

# Variables de sesión para controlar el flujo
if "version_confirmada" not in st.session_state:
    st.session_state.version_confirmada = False  # No se ha confirmado la versión aún

if "data_source" not in st.session_state:
    st.session_state.data_source = None

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Función para cargar dinámicamente una versión
def cargar_version(version):
    try:
        modulo = importlib.import_module(f"proyectos.{version}.principal")  
        return modulo
    except ImportError as e:
        st.error(f"Error al cargar la versión {version}: {e}")
        return None

# Función para ejecutar la versión seleccionada
def ejecutar_version(version):
    modulo = cargar_version(version)
    if modulo:
        st.success(f"Ejecutando {version}...")
        modulo.ejecutar()
    else:
        st.error(f"No se pudo cargar la versión {version}")

# Interfaz de Streamlit
def main():
    st.title("Selector de Versiones")

    # 1️⃣ Primero seleccionas la versión
    version = st.selectbox(
        "Selecciona la versión que deseas ejecut
