import json
from pathlib import Path
import platform


import m_carga_config

configuracion = m_carga_config.cargar_configuracion()


def m_guardar_json(mi_diccionario, mi_archivo_json):
    # Directorio donde deseas guardar el archivo
    
    sistema_operativo = platform.system()
    if sistema_operativo == "Windows":
        path_arch_json = "C:" + configuracion["path_arch_json"] + mi_archivo_json
    else:
        path_arch_json = configuracion["path_arch_json"] + mi_archivo_json
    print(f"Ruta completa del archivo: {path_arch_json}")
    directorio_destino = Path(path_arch_json)

    # Guardar el diccionario en el archivo JSON
    with open(path_arch_json, 'w', encoding='utf-8') as archivo_json:
        json.dump(mi_diccionario, archivo_json, indent=4)

    print(f"Diccionario guardado en: {path_arch_json}")

