from supabase import create_client, Client
import os
import streamlit as st

def inicializar_supabase() -> Client:
    """
    Obtiene las credenciales de Supabase desde las variables de entorno
    y crea una instancia del cliente de Supabase.
    """
    try:
        # Obtener las credenciales desde las variables de entorno
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        # Validar que las credenciales estén configuradas
        if not supabase_url or not supabase_key:
            raise ValueError("Las variables de entorno SUPABASE_URL y SUPABASE_KEY no están configuradas.")

        # Crear el cliente de Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        return supabase

    except Exception as e:
        st.error(f"Error al inicializar Supabase: {e}")
        raise  # Re-lanzar la excepción para que el programa se detenga si hay un error crítico