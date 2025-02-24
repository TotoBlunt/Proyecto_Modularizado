
import streamlit as st
import importlib

# Función para cargar dinámicamente el módulo principal
def cargar_modulo():
    try:
        modulo = importlib.import_module("Proyecto2.principal")  # Carga principal.py
        return modulo
    except ImportError as e:
        st.error(f"Error al cargar el módulo: {e}")
        return None

# Función para ejecutar la lógica principal
def ejecutar_aplicacion():
    modulo = cargar_modulo()
    if modulo:
        st.success("Aplicación cargada correctamente.")
        modulo.ejecutar()  # Llama a la función ejecutar() del módulo principal
    else:
        st.error("No se pudo cargar la aplicación.")

# Interfaz de Streamlit
def main():
    ejecutar_aplicacion()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()