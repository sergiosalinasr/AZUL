from a_OpenAI_Cred import credenciales_openai
import inspect
from flask import Flask, jsonify, request
import m_logging
from openai import OpenAI
import pandas as pd
import json
import pickle
import m_carga_config

configuracion = m_carga_config.cargar_configuracion()

def auth(usuario, password):
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    
    if ( usuario != "sergio.salinasr@gmail.com" ) or ( password != "123456" ) :
        dict_respuesta = {
                'status': "error",
                'result': { 'error_id': 200, 'error_msg': "El usuario y/o password es invalido"}
                }
    else:
        dict_respuesta = {
                'status': "ok",
                'result': { 'token': "AquiVaUnToken"}
                }

    return dict_respuesta


if __name__ == "__main__":
    
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
   
    textos_csv = configuracion["textos_csv"]["path_arch_csv"] +  configuracion["textos_csv"]["textos_csv"]
    
    archivo_textos_csv = input(f"Ingresar archivo de texto csv de input (Enter para usar [{textos_csv}]): ") or textos_csv

    print(embed_text(archivo_textos_csv))