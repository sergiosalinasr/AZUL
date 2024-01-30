import json
import os

def cargar_configuracion():
    with open('src/config.json', 'r') as f:
        return json.load(f)

def crear_carpeta(str_carpeta):

    # Verificar si la carpeta existe
    if not os.path.exists(str_carpeta):
        # Si no existe, crear la carpeta
        os.makedirs(str_carpeta)
        print(f'Se ha creado la carpeta: {str_carpeta}') 

def carpetas_base():

    configuracion = cargar_configuracion()

    # Ruta del archivo csv de input
    str_carpeta = "/tmp"
    crear_carpeta(str_carpeta)

    carpeta_tmp_BORRAR = configuracion["tmp_BORRAR"]
    crear_carpeta(carpeta_tmp_BORRAR)

    carpeta_TXTFiles = carpeta_tmp_BORRAR + configuracion["TXTFiles"]
    crear_carpeta(carpeta_TXTFiles)

    carpeta_JSONFiles = carpeta_tmp_BORRAR + configuracion["JSONFiles"]
    crear_carpeta(carpeta_JSONFiles)

    carpeta_BINFiles = carpeta_tmp_BORRAR + configuracion["BINFiles"]
    crear_carpeta(carpeta_BINFiles)

    '''
    "TXTFiles" : "TXTFiles/",
    "JSONFiles" : "JSONFiles/",
    "BINFiles" : "BINFiles/",
    '''

