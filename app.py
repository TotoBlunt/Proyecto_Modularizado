import streamlit as st
import importlib
import sys
import os
import pandas as pd
from proyectos.Proyecto2.FrontEnd.estilos_st import aplicar_estilos
from scripts.integrantes import mostrar_integrantes


# Variables de estado
if "version_seleccionada" not in st.session_state:
    st.session_state.version_seleccionada = None  # Ahora empieza sin versión seleccionada

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
        "Selecciona la versión que deseas ejecutar:",
        options=["Proyecto1", "Proyecto2"],  
        index=0  
    )

    if version != st.session_state.version_seleccionada:
        st.session_state.version_seleccionada = version
        st.session_state.data_source = None  # Reiniciar selección de datos

    # 2️⃣ Luego seleccionas la fuente de datos (solo si hay versión)
    if st.session_state.version_seleccionada:
        st.subheader("Seleccionar fuente de datos")
        data_option = st.radio("¿Desde dónde quieres cargar el modelo?", ["Supabase", "CSV/Excel"])

        if data_option != st.session_state.data_source:
            st.session_state.data_source = data_option  # Guardar selección

        # 3️⃣ Solo si eliges "CSV/Excel" te muestra la opción de subir archivos
        if st.session_state.data_source == "CSV/Excel":
            archivo = st.file_uploader("Carga tu archivo CSV o Excel", type=["csv", "xlsx"])
            if archivo:
                st.session_state.uploaded_file = archivo  # Guardar el archivo
                try:
                    if archivo.name.endswith(".csv"):
                        df = pd.read_csv(archivo)
                    else:
                        df = pd.read_excel(archivo)
                    st.write(df)  # Mostrar los datos
                except Exception as e:
                    st.error(f"Error al leer el archivo: {e}")

    # 4️⃣ Solo habilitar el botón si hay versión seleccionada
    if st.session_state.version_seleccionada and st.button("Ejecutar Versión"):
        ejecutar_version(st.session_state.version_seleccionada)

if __name__ == "__main__":
    # Configurar el ancho de la página
    st.set_page_config(layout="wide")

    # Aplicar estilos personalizados
    aplicar_estilos()

    # Dividir la pantalla en dos secciones (20% izquierda, 80% derecha)
    col1, col2 = st.columns([2, 8])

    # Sección de integrantes del grupo (20% - izquierda)
    with col1:
        mostrar_integrantes()

    # Sección principal (80%)
    with col2:
        main()
