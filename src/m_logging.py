
import m_carga_config

import logging
from logging.handlers import RotatingFileHandler
import platform
import os
import shutil
from datetime import datetime


configuracion = m_carga_config.cargar_configuracion()

#print(f'El valor de parametro1 es: {configuracion["parametro1"]}')


def m_logging():
    # Crear un formateador de logs
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')

    # Obtener el objeto logger
    logger = logging.getLogger()

# Crear un manejador para mensajes INFO
    log_file_INFO = configuracion["log_file_INFO"]
    sistema_operativo = platform.system()
    if sistema_operativo == "Windows":
        log_file_INFO = "C:" + configuracion["log_file_INFO"]
    
    # Añadir los manejadores solo si el logger no tiene ninguno
    if not logger.handlers:

        file_handler_info = logging.FileHandler(log_file_INFO)
        file_handler_info.setLevel(logging.INFO)
        file_handler_info.setFormatter(log_formatter)

        # Añadir los manejadores al logger
        logger.addHandler(file_handler_info)

        # Configurar el nivel de registro del logger
        logger.setLevel(logging.INFO)

        file_handler_info.close()

def logging_respaldo():
    log_file_INFO = configuracion["log_file_INFO"]
    sistema_operativo = platform.system()
    if sistema_operativo == "Windows":
        log_file_INFO = "C:" + configuracion["log_file_INFO"]

    # respaldar el archivo de log si supera los 5MB
    
    if os.path.exists(log_file_INFO) and os.path.getsize(log_file_INFO) > 1024:
        now = datetime.now()
        # Formatear la fecha y hora en el formato deseado
        formatted_datetime = now.strftime("%Y%m%d%H%M%S")
        backup_file = log_file_INFO + formatted_datetime
        shutil.copy(log_file_INFO, backup_file)
        # Abrir el archivo en modo escritura para vaciarlo
        with open(log_file_INFO, 'w') as archivo:
            pass

def msg_logging(msg):
    # Verificar si corresponde respaldar el archivo de log
    logging_respaldo()

    # Crear un formateador de logs
    m_logging()
    logger = logging.getLogger()
    logger.info(msg)
