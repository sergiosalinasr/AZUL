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

def embed_text(pathName_csv):
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    credenciales_openai()
    conocimiento_df = pd.read_csv(pathName_csv)
    
    client = OpenAI()

    conocimiento_df['Embedding'] = conocimiento_df['texto'].apply(lambda x: client.embeddings.create(input=x, model="text-embedding-ada-002"))

    embeddings_pkl = configuracion["arch_bin"]["path_arch_bin"] +  configuracion["arch_bin"]["embed_pkl"]

    # Guardar el objeto en un archivo binario
    with open(embeddings_pkl, 'wb') as archivo:
        pickle.dump(conocimiento_df, archivo)

    #conocimiento_df.to_csv(embeddings_csv)

    dict_respuesta = {
            'Archivo_csv_procesado': pathName_csv,
            'Archivo_de_salida': embeddings_pkl
            }

    return dict_respuesta


if __name__ == "__main__":
    
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
   
    textos_csv = configuracion["textos_csv"]["path_arch_csv"] +  configuracion["textos_csv"]["textos_csv"]
    
    archivo_textos_csv = input(f"Ingresar archivo de texto csv de input (Enter para usar [{textos_csv}]): ") or textos_csv

    print(embed_text(archivo_textos_csv))