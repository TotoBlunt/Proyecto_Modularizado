from sklearn.ensemble import VotingRegressor,RandomForestRegressor,GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import openpyxl
import pandas as pd 
import streamlit as st
import numpy as np
from datetime import datetime
from scripts.CRUD import crear_prediccion
import json
from scripts.supabase_connector import inicializar_supabase
import pickle

Client = inicializar_supabase()

#Titulo para el app
st.title("Proyecto Productivo para la prediccion del peso de pollos usando variables descritas por el modelo SelectcKbest luego hacer las predicciones usando el Modelo Ensemble, con Streamlit(v1)")

def obtener_datos_desde_supabase():
    """
        Desde SUPABASE se obtine los datos mediante la conexion ya realizada anteriormente
        para poder hacerlo de una manera automatica
    """
    # Nombre de la tabla de Supabase
    tabla = 'DatosPredicciones'

    try:
        # Obtener los datos de la tabla
        response = Client.table(tabla).select("*").execute()

        # Crear el DataFrame
        df = pd.DataFrame(response.data)

        # Verificar si el DataFrame está vacío
        if df.empty:
            st.error("El DataFrame está vacío.")
            return None

        # Mostrar los datos
        st.write('### Vista previa de los datos desde Supabase')
        st.write(df.head())

        return df
    except Exception as e:
        st.error(f"Error al obtener datos desde Supabase: {e}")
        return None

def subir_archivo():

    """
    Seleccionar archivos desde el entorno local para poder usarlo previamente se debe tener el archivo CSV o EXCEL
    descargado en la PC
    
    """
    # Subir archivo de excel o csv
    upload_file = st.file_uploader('Sube un archivo Excel o CSV', type=['xlsx', 'csv'])

    # Inicializar df como None
    df = None

    if upload_file is not None:
        try:
            # Cargar archivos y determinar cual es
            if upload_file.name.endswith('.xlsx'):
                df = pd.read_excel(upload_file)
            elif upload_file.name.endswith('.csv'):
                df = pd.read_csv(upload_file,sep=';')
            else:
                st.error("Formato de archivo no soportado. Por favor, sube un archivo Excel (xlsx) o CSV (csv).")

            if df is not None:
                st.write('### Vista previa de los datos')
                st.write(df.head())
        except FileNotFoundError as e:
            st.error(f"Error en el proceso: {e}")
        except SyntaxError as e:
            st.error(f"Error de Sintaxis: {e}")
        except Exception as e:
            st.error(f"Error inesperado: {e}")

    return df

def seleccion_variables(df):

    """
    Esta funcion selecciona las variuables importantes mediante el selectKbest para realizar
    el grafico de importancias y seleccionar las variables a usar en el modelo de prediccion
    """

    try:
        # Convertir variables categóricas a valores numéricos
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            
        # Excluir la columna IEP de la selección inicial
        X = df.drop(['PesoFinal', 'SiNoPesoFinal', 'ICA', 'IEP', 'GananciaDiaVenta', 'DiasSaca', 'EdadGranja',
                    'ConsumoFinalizador', 'PesoStd', 'Nzona', 'StdConsAve'], axis=1)  # Todas las variables menos PesoFinal, SiNoPesoFinal e IEP
        y = df['SiNoPesoFinal']  # Variable objetivo (Si/No)

        # Seleccionar las 20 variables más importantes (excluyendo IEP)
        selector = SelectKBest(f_classif, k=20)
        selector.fit(X, y)

        # Obtener las variables seleccionadas y asegurarse de que IEP no esté incluido
        selected_features = X.columns[selector.get_support()]

        # Si IEP está dentro de las 20 principales, añadir la siguiente mejor característica
        k = 20
        while 'IEP' in selected_features:
            k += 1
            selector = SelectKBest(f_classif, k=k)
            selector.fit(X, y)
            selected_features = X.columns[selector.get_support()]

        # Imprimir las variables seleccionadas
        st.write("#### Características seleccionadas:", pd.DataFrame(selected_features))

        # Crear y entrenar un modelo de aprendizaje
        X_train, X_test, y_train, y_test = train_test_split(X[selected_features], y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        st.write('### Métrica de Evaluación para el Modelo RandomForestClassifier de Importancias')
        st.write(f'#### Accuracy: {accuracy_score(y_test, y_pred):.4f}')
        st.write(f'#### Promedio de la Validación Cruzada: {cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy").mean():.4f}')

        # Importancia de las características
        importances = model.feature_importances_
        feature_importances = pd.DataFrame({'Característica': selected_features, 'Importancia': importances})
        feature_importances = feature_importances.sort_values('Importancia', ascending=False)
        
        # Gráfico de importancia
        # Crear el diagrama de barras
        fig, ax = plt.subplots()
        ax.barh(feature_importances['Característica'], feature_importances['Importancia'])
        ax.set_xlabel('Importancia')
        ax.set_ylabel('Característica')
        ax.set_title('Importancia de las 20 Características Principales')
        st.pyplot(fig)

        # Sugerencias para mejorar el objetivo "SI"
        st.write("### Para mejorar el logro del objetivo 'SI' en PesoFinal, concéntrate en mejorar las siguientes 5 variables principales:")
        cont = 0
        for feature, importance in feature_importances.itertuples(index=False):
            st.write(f"- {feature} (Importancia: {importance:.3f})")
            cont += 1
            if cont == 5:
                break
        # Variables más importantes a trabajar en el modelo
        top5 = feature_importances['Característica'].head(5)
        top5 = top5.tolist()
        st.write(f'#### Variables a utilizar en el modelo: ', top5)

        return top5
    except KeyError as e:
        st.error(f"Error: La columna '{e.args[0]}' no se encuentra en el DataFrame.")
    except Exception as e:
        st.error(f"Error inesperado: {e}")

def modelo_ensemble(top5,df):

    """
    Funcion netamente de prediccion entrenamiento del modelo y posterior prediccion
    """
        
    #DIVIR EL DATA FRAME EN CARACTERISTICAS Y ETIQUETAS PARA ENTRENAR EL MODELO
    x_model = df[top5] #Cuando es mas de una columna se utiliza dos corchetes para que lo lea correctamente
    y_model = df['PesoFinal'] 
        
    #Conjuntpo de Pruebas
    # Dividir los datos en conjunto de entrenamiento y prueba
    x_train_model, x_test_model, y_train_model, y_test_model = train_test_split(x_model, y_model, test_size=0.3, random_state=42)

        
    #Crear una lista de modelos
    models = [ ("decision_tree", DecisionTreeRegressor(max_depth=5,random_state=42)),
         ("linear_regression",LinearRegression()), 
         ("k_neighbors",KNeighborsRegressor(n_neighbors=5,weights='distance')),
         ("random_forest",RandomForestRegressor(n_estimators=10,min_samples_split=3,max_depth=6,random_state=42)),
         ('gradient_booster',GradientBoostingRegressor(n_estimators=10,random_state=42))] #de los 5 vecinos sacara deciciones estadisticas

    # Crear un modelo de ensamble con los modelos anteriores el metodo combina las predicciones de varios modelos 
    modelo = VotingRegressor(models)

    #Entrenar el modelo con los datos
    modelo.fit(x_train_model,y_train_model)

    # Hacer predicciones con el modelo usando datos de prueba
    y_pred_model = modelo.predict(x_test_model)

    #Crear una nueva colmuna en el df
    df['Peso Prom Final Predicho'] = modelo.predict(x_model)
    return modelo,y_pred_model,y_test_model,x_train_model,y_train_model
        

def menu_opciones(modelo, y_pred_model, y_test_model, df, x_train_model, y_train_model):

    """
    Funcion para mostrar grafico de comparaciones , metricas de evaluacion y realizar las predicciones con 
    datos ingresados por el usuario en este aparatado se esta utilizando el modelo previamente entrenado
    """

    # Inicializar datos como None
    input_data, datos = [], {}

    # Selección de página
    page = st.radio(
        "### Selecciona una opción",
        ["Predicción", 'Grafico de Comparacion en la Prediccion', 'Metricas de Evaluacion del Modelo']
    )

    # Guardar la opción seleccionada en el estado de sesión
    st.session_state['opcion_seleccionada'] = page

    if page == 'Metricas de Evaluacion del Modelo':
        # Calcular métricas de evaluación
        st.write('### Metricas de Evaluacion del "Modelo Final(VotingRegresor)":\n')
        mse = mean_squared_error(y_test_model, y_pred_model)
        r2 = r2_score(y_test_model, y_pred_model)
        mae = mean_absolute_error(y_test_model, y_pred_model)
        st.write(f'#### Coeficiente de determinacion(R²): {r2:.4f}')
        st.write(f'#### Error cuadratico medio(MSE): {mse:.4f}')
        st.write(f'#### Error absoluto medio(MAE): {mae:.4f}')
        # Validación Cruzada del modelo Voting
        r2_scores = cross_val_score(modelo, x_train_model, y_train_model, cv=5, scoring='r2')
        st.write(f'#### R² promedio en validación cruzada: {r2_scores.mean():.4f}')

    elif page == 'Grafico de Comparacion en la Prediccion':
        st.write('### Grafico de Comparacion en la Prediccion')
        # Grafico de Comparacion
        fig, ax = plt.subplots()
        ax.plot(df['PesoFinal'], label='Peso Prom. Final (Real)', color='blue')
        ax.plot(df['Peso Prom Final Predicho'], label='Peso Prom. Final Predicho', color='red')
        ax.set_xlabel('Índice')
        ax.set_ylabel('Peso Prom. Final')
        ax.set_title('Comparación entre Peso Prom. Final Real y Predicho')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # Varianza
        varianza = ((df['PesoFinal'] - df['Peso Prom Final Predicho']) ** 2).mean()
        st.write(f"#### La varianza de los valores es:  {varianza:.4f}")

    elif page == "Predicción":
        st.title("Aplicación de Prediccion")
        # Entradas de datos para las características
        feature_1 = float(st.number_input('Ingresa el valor para PesoSem4', format="%.3f"))
        feature_2 = float(st.number_input('Ingresa el valor para Agua', format="%.3f"))
        feature_3 = float(st.number_input('Ingresa el valor para PesoSem3', format="%.3f"))
        feature_4 = float(st.number_input('Ingresa el valor para ConsumoAcabado', format="%.3f"))
        feature_5 = float(st.number_input('Ingresa el valor para MortStd', format="%.3f"))
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formato más limpio
        nombre = st.text_input('Ingrese su nombre')

        if feature_1 is not None and feature_2 is not None and feature_3 is not None and feature_4 is not None and feature_5 is not None:
            # Crear el array con los datos de entrada
            input_data = np.array([[feature_1, feature_2, feature_3, feature_4, feature_5]])
            # Diccionario
            datos = {
                'peso_sem4': feature_1,
                'agua': feature_2,
                'peso_sem3': feature_3,
                'consumo_acabado': feature_4,
                'mortalidad_std': feature_5,
                'created_at': created_at,
                'nombre': nombre
            }
        else:
            st.error("### Por favor, ingresa valores válidos para todas las características.")

    return input_data, datos
    
def prediccion(modelo,input_data,datos):

    """Esta funcion guarda los datos previamente incluidos 
    y realiza la prediccion para guardalo en el data frame que se guardara en el SUPABASE
    """

    prediction = modelo.predict(input_data)
    prediction = round(prediction[0], 2)  # Formato de dos decimales
    # Diccionario
    datos['prediction'] = prediction
    datos = json.dumps(datos)
    # Mostrar el resultado de la predicción
    st.write(f'### La predicción del modelo para Peso Final es : {prediction} kg')
    #st.write(datos)
    return datos  
        
def guardar_modelo(modelo,ruta):
    """
    Se guardara el modelo creado en un pkl para su futura 
    utilizacion, donde indicaras como parametro el modelo entrenado
    y la ruta que le daras para su futura utilizacion
    """
    with open(ruta, 'wb') as archivo:
        pickle.dump(modelo, archivo)
        
def cargar_modelo(ruta):
    """Carga un modelo desde un archivo .pkl  indicada como parametro de la funcion"""
    with open(ruta, 'rb') as archivo:
        return pickle.load(archivo)