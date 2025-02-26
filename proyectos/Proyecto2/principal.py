from .modelo import obtener_datos_desde_supabase, seleccion_variables, modelo_ensemble, menu_opciones, prediccion,subir_archivo
from scripts.CRUD import crear_prediccion, listar_registros, verificar_registros, eliminar_prediccion_rpc
import streamlit as st
from proyectos.Proyecto2.FrontEnd.estilos_st import aplicar_estilos
from scripts.integrantes import mostrar_integrantes

def ejecutar():
    #VErsion
    st.title("_____Version_2_____")


    # Estado de sesión para manejar datos entre interacciones
    if 'datos_edit' not in st.session_state:
        st.session_state['datos_edit'] = None

    # Estado para controlar si se ha pulsado "Eliminar"
    if 'mostrar_lista_y_campo_id' not in st.session_state:
        st.session_state['mostrar_lista_y_campo_id'] = False

    # Cargar archivo
    st.title("Cargar datos para predicción")
    st.write("Selecciona cómo deseas cargar los datos:")

    # Opciones para el usuario
    opcion = st.selectbox(
        "Elige una opción:",
        ("Subir archivo manualmente", "Cargar datos desde Supabase")
    )

    # Lógica para manejar la opción seleccionada
    if opcion == "Subir archivo manualmente":
        df = subir_archivo()
    else:
        df = obtener_datos_desde_supabase()


    if df is not None:
        #Datos del Dataframe
        st.write("### Datos cargados correctamente")
        st.write("Total de filas:", len(df))
        st.write("Total de columnas:", len(df.columns))

        # Selección de las mejores variables
        top5 = seleccion_variables(df)
        if top5:
            # Entrenamiento del modelo ensemble
            modelo, y_pred_model, y_test_model, x_train_model, y_train_model = modelo_ensemble(top5, df)

            # Menú de opciones (Predicción, Métricas, Gráfico, etc.)
            input_data, datos = menu_opciones(modelo, y_pred_model, y_test_model, df, x_train_model, y_train_model)

            # Mostrar botones solo si la opción seleccionada es "Predicción"
            if st.session_state.get('opcion_seleccionada') == "Predicción":
                # Botón para realizar predicción
                if st.button('Realizar Predicción'):
                    # Generar predicción y guardar en el estado de sesión
                    st.session_state['datos_edit'] = prediccion(modelo, input_data, datos)

                # Verificar si hay datos disponibles para guardar
                if st.session_state['datos_edit'] is not None:
                    # Botón para guardar los datos en Supabase
                    if st.button('Guardar'):
                        crear_prediccion(st.session_state['datos_edit'])
                        st.success('Datos guardados correctamente en Supabase.')
                        # Limpiar el estado después de guardar
                        st.session_state['datos_edit'] = None

                # Botones para listar y eliminar registros
                if verificar_registros():
                    if st.button('Listar Registros'):
                        listar_registros()

                    # Botón "Eliminar"
                    if st.button('Eliminar'):
                        st.write('Lista los Registros para verificar el ID a eliminar')
                        # Cambiar el estado para mostrar la lista y el campo de ID
                        st.session_state['mostrar_lista_y_campo_id'] = True

                    # Mostrar la lista y el campo de ID solo si se ha pulsado "Eliminar"
                    if st.session_state['mostrar_lista_y_campo_id']:
                
                        # Campo para ingresar el ID a eliminar
                        prediccion_id = st.number_input("Ingresa el ID del registro que deseas eliminar:", min_value=0)

                        # Botón para confirmar la eliminación
                        if st.button('Eliminar Registro'):
                            if prediccion_id > 0:  # Asegurarse de que el ID sea válido
                                if eliminar_prediccion_rpc(int(prediccion_id)):
                                    st.success(f"Registro con ID {prediccion_id} eliminado correctamente.")
                                    # Reiniciar el estado para ocultar la lista y el campo de ID
                                    st.session_state['mostrar_lista_y_campo_id'] = False
                                    st.rerun()  # Recargar la página para actualizar la lista
                            else:
                                st.error("Por favor, ingresa un ID válido.")

    else:
        st.write("No se ha cargado ningún archivo.")

if __name__ == "__main__":
    obtener_datos_desde_supabase()