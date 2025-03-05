# Proyecto Modularizado con Streamlit
Ruta Streamlit: https://version2idl2.streamlit.app/

¡Bienvenido al repositorio del **Proyecto Modularizado con Streamlit**! Este proyecto es una aplicación interactiva que permite ejecutar diferentes versiones de un programa desde una interfaz única, con la finalidad de predecir el peso final de aves en un entorno controlado. Además, incluye un sistema de logging para rastrear el comportamiento de la aplicación y manejar errores.


## 📋 Descripción

Este proyecto está diseñado para manejar múltiples versiones de un programa de manera modular. Cada versión tiene su propia lógica y se puede seleccionar dinámicamente desde la interfaz de Streamlit. También incluye un sistema de logging para registrar eventos importantes y facilitar la depuración.


## 🚀 Características

- **Selección de Versiones**: Elige entre diferentes versiones del programa desde una interfaz amigable.
- **Modularidad**: Cada versión está encapsulada en su propio módulo, lo que facilita la mantenibilidad y escalabilidad.
- **Interactividad**: Usa Streamlit para crear una interfaz web interactiva y fácil de usar.
- **Logging**: Registra eventos importantes en archivos de log para facilitar la depuración y el monitoreo.
- **Carga de Archivos**: Permite cargar datos desde Supabase o archivos CSV/Excel.


## 🛠️ Instalación

Sigue estos pasos para instalar y ejecutar el proyecto en tu máquina local:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/TotoBlunt/Proyecto_Modularizado.git
   ```
2. **Navega al directorio del proyecto**:
    ```bash
    cd Proyecto_Modularizado
    ```
3. **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Ejecuta la aplicación**:
    ```bash
    streamlit run app.py
    ```
5. **Abre tu navegador**.
    * La aplicacion estara disponible en http://localhost:8501.

6. **Ingresa directamente**:
    * Ruta Streamlit: https://version2idl2.streamlit.app/

## 🗂️ Estructura del Proyecto 
    
    |Logs/
    |Private/
    |Proyectos/
    |-----|Proyecto1/
    |---------------|__init__.py
    |---------------|Principal.py
    |-----|Proyecto2/
    |---------------|FrontEnd/
    |-------------------------|__init__,.py
    |-------------------------|estilos_st.py
    |---------------|__init__.py
    |---------------|Modelo.py
    |---------------|Principal.py
    |Scripts/
    |-----|__init__.py
    |-----|CRUD.py
    |-----|App_verificar_logs.py
    |-----|Integrantes.py
    |-----|Logger.py
    |-----|Supabase_connector.py
    |	
    |. gitignore
    |LICENSE	
    |README.md
    |App.py
    |Requirements.txt
    
**Carpetas**:

* Logs : En esta carpeta se guardaron los scripts para realizar y revisar los logs debido a que streamlit tiene su propia base de datos para mostrar estos logs, se usaran de una manera online.
* Private : En esta carpeta se guardarán datos sensibles que no se deben mostrar al público en general, la cual será agregada al. gitignore para dicho fin.
* Proyectos : En esta carpeta se mostrarán los proyectos que vienen a ser las distintas versiones del mismo, en la cual se incluyen el Proyecto1 y Proyecto2, las cuales incluyen los scripts necesarios para la realización del modelo.
* Scripts : En esta carpeta se incluyó los scripts que se pueden reutilizar en todas las versiones del modelo, esto se realizó para que el proyecto sea escalable y no se esté reescribiendo código.

**Archivos**:

* gitignore : Este archivo contiene las carpetas con información sensible para que no sea vista por el público en general.
*  license : Este archivo se incluyó para la protección de derechos, fomentar la colaboración y promover el uso del código.
*README : Se incluyo este archivo ya que es la portada de lo que viene a ser nuestro repositorio y explica que es y cómo usar nuestro proyecto.
* app.py : Este archivo es el principal desde donde correrán nuestras versiones es el que se muestra en el streamlit y nos brinda todo el ecosistema del proyecto.
* requirements : Este archivo contiene las bibliotecas necesarias para el buen funcionamiento del proyecto, las cuales se irán actualizando conforme el proyecto lo requiera.
* init.py : Este archivo es una herramienta clave para la organización de código en Python, permite identificar directorios como paquetes y facilita la gestión de importaciones y la inicialización de módulos, normalmente se usa vacio.

## 📝 Uso

1. **Selecciona una versión**:

    * Al ejecutar la aplicación, verás un menú desplegable para seleccionar la versión que deseas usar.

2. **Carga los datos**:

    * Elige si deseas cargar los datos desde Supabase o desde un archivo CSV/Excel.

3. **Ejecuta el modelo**:

    * El modelo se ejecutara automaticamemnte y se mostrara un menu donde podra escoger la accion a realizar dependiendo la version elegida.

## 📂 Versiones disponibles

* **Versión 1**: Esta version incluye la carga desde un archivo Excel o CSV, y nos da la opcion de realizar una prediccion, verificar las metricas de evaluacion del modelo y la grafica de los datos reales vs los datos predichos.

* **Versión 2**: Esta version adiciona la carga de datos automatizada desde el supabase con una BD preestabelcida para dicho fin, adicionalmente a ello en esa version podemos crear,guardar y eliminar las predicciones en una base de datos configurada en supabase.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo LICENSE.

## 🙌 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, sigue estos pasos:

1.Haz un fork del repositorio.

2.Crea una rama con tu nueva funcionalidad (git checkout -b feature/nueva-funcionalidad).

3.Haz commit de tus cambios (git commit -m 'Agrega nueva funcionalidad').

4.Haz push a la rama (git push origin feature/nueva-funcionalidad).

5.Abre un Pull Request.

## 📧 Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactarnos:

° Email: totoblunt15@gmail.com

° GitHub: https://github.com/TotoBlunt