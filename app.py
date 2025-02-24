# main.py
import streamlit as st
import importlib
import sys
import os
from proyectos.Proyecto2.FrontEnd.estilos_st import aplicar_estilos
from scripts.integrantes import mostrar_integrantes

# Agrega la carpeta "private" al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "private"))

# Función para cargar dinámicamente una versión
def cargar_version(version):
    try:
        modulo = importlib.import_module(f"proyectos.{version}.principal")  # Carga principal.py de la versión
        return modulo
    except ImportError as e:
        st.error(f"Error al cargar la versión {version}: {e}")
        return None

# Función para ejecutar la versión seleccionada
def ejecutar_version(version):
    modulo = cargar_version(version)
    if modulo:
        st.success(f"Ejecutando {version}...")
        modulo.ejecutar()  # Llama a la función ejecutar() de la versión seleccionada
    else:
        st.error(f"No se pudo cargar la versión {version}")

# Interfaz de Streamlit
def main():
    st.title("Selector de Versiones")

    # Selector de versión
    version_seleccionada = st.selectbox(
        "Selecciona la versión que deseas ejecutar:",
        options=["Proyecto1", "Proyecto2"],  # Opciones disponibles
        index=0  # Versión predeterminada
    )

    # Botón para ejecutar la versión seleccionada
    if st.button("Ejecutar Versión"):
        ejecutar_version(version_seleccionada)

# Punto de entrada de la aplicación
# Configurar el ancho de la página
    st.set_page_config(layout="wide")

    # Aplicar estilos personalizados
    aplicar_estilos()

    # Dividir la pantalla en dos secciones (20% izquierda, 80% derecha)
    col1, col2 = st.columns([2, 8])

    # Sección de integrantes del grupo (20% - izquierda)
    with col1:
        st.title("Integrantes del Grupo")

        mostrar_integrantes()

    # Sección principal (80%)
    with col2:
        if __name__ == "__main__":
            main()