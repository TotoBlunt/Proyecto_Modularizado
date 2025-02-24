import importlib

def cargar_version(version):
    try:
        modulo = importlib.import_module(f"{version}.modulo_principal")
        return modulo
    except ImportError as e:
        print(f"Error al cargar la versión {version}: {e}")
        return None

def ejecutar_version(version):
    modulo = cargar_version(version)
    if modulo:
        print(f"Ejecutando {version}...")
        modulo.ejecutar()  # Suponiendo que cada versión tiene una función `ejecutar`
    else:
        print(f"No se pudo cargar la versión {version}")

if __name__ == "__main__":
    # Cambia esta variable para ejecutar una versión u otra
    version_a_ejecutar = "version_1"  # Puedes cambiar a "version_2" o "version_3"

    ejecutar_version(version_a_ejecutar)