import streamlit as st
from logger import activity_logger, warning_logger, error_logger

st.title("Sistema de Logging en Streamlit")

data_input = st.text_input("Ingrese un valor:")

type_of_log = st.selectbox("Seleccione el tipo de log a generar", ["Actividad", "Advertencia","Error"])

if st.button("Generar Log"):
    if type_of_log == "Actividad":
        activity_logger.info(f"Usuario Ingresó: {data_input}")
        st.success("Log de actividad Generado")
    elif type_of_log == "Advertencia":
        warning_logger.warning(f"Posible problema con el dato: {data_input}")
        st.warning("Log de advertencia Generado")
    elif type_of_log == "Error":
        error_logger.error(f"Error detectado con el dato: {data_input}")
        st.error("Log de error generado")