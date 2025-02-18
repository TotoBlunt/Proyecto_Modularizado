import streamlit as st
#Interfaz de Strreamlit


def aplicar_estilos():

    st.markdown(
        """
        <style>
        /* Estilos generales */
        .stApp {
            background-color: #F5F5F5 !important; /* Color de fondo de la aplicación */
            color: #333333 !important; /* Color del texto principal */
        }

        /* Estilos para botones */
        .stButton button {
            background-color: #4CAF50 !important; /* Color de fondo del botón */
            color: white !important; /* Color del texto del botón */
            border-radius: 5px !important; /* Bordes redondeados */
            border: none !important; /* Sin borde */
            padding: 10px 20px !important; /* Espaciado interno */
        }

        /* Estilos para inputs */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #FFFFFF !important; /* Color de fondo del input */
            color: #333333 !important; /* Color del texto del input */
            border-radius: 5px !important; /* Bordes redondeados */
            border: 1px solid #CCCCCC !important; /* Borde sutil */
            padding: 10px !important; /* Espaciado interno */
        }

        /* Estilos para mensajes */
        .stSuccess {
            color: #4CAF50 !important; /* Color del texto en mensajes de éxito */
        }
        .stError {
            color: #FF5252 !important; /* Color del texto en mensajes de error */
        }

        /* Estilos para la división de la pantalla */
        .sidebar .sidebar-content {
            width: 30% !important; /* Ancho del sidebar */
            background-color: #FFFFFF !important; /* Color de fondo del sidebar */
            padding: 20px !important; /* Espaciado interno */
            box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1) !important; /* Sombra sutil */
        }

        .main .block-container {
            width: 70% !important; /* Ancho del contenido principal */
            padding: 20px !important; /* Espaciado interno */
        }
        </style>
        """,
        unsafe_allow_html=True
    )