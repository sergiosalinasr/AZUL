from a_OpenAI_Cred import credenciales_openai
import inspect
import m_logging
from openai import OpenAI
import pandas as pd
import numpy as np
import ast  # Módulo para analizar cadenas JSON
import pickle
import m_carga_config

configuracion = m_carga_config.cargar_configuracion()

# Funcione que calcula la similaridad a partir de dos array numpy
def cosine_similarity_np(a, b):
    
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Funcione que calcula la similaridad a partir de dos objetos openai.Embedding
def cosine_similarity(a, b):
    
    # Obtiene los vectores de embedding
    b_vector = b.data[0].embedding
    b = np.array(b_vector)
    a_vector = a.data[0].embedding
    a = np.array(a_vector)
   
    
    return cosine_similarity_np(a, b)

def chat_completion(messages):
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    try:
        print("Ini Completation...")
        client = OpenAI()

        #response = client.ChatCompletion.create(
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=1000
        )
        print("fin completation")
        if response.choices and response.choices[0].message:
            #return response.choices[0].message["content"]
            return response.choices[0].message.content
        else:
            return None
    except Exception as error:
        print("error en completation")
        if hasattr(error, 'response') and error.response:
            print(error.response.status_code)
            print(error.response.json())
        else:
            print(error)
        return None

def responder_la_pregunta(pregunta, documentos):
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')

    textos = "Eres un consultor útil.\n" + documentos['texto'].str.cat(sep='\n ')
    
    messages = [
        {"role": "system", "content": textos},
        {"role": "user", "content": pregunta},
    ]

    respuesta = chat_completion(messages)

    return respuesta


def pregunta_y_respuesta(txt_pregunta, embeddings_pkl, n_resultados):
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    credenciales_openai()
    client = OpenAI()
    pregunta_embed = client.embeddings.create(input=txt_pregunta, model="text-embedding-ada-002")
    
    # Cargar el objeto desde el archivo binario
    with open(embeddings_pkl, 'rb') as archivo:
        datos = pickle.load(archivo)

    

    datos["Similitud"] = datos['Embedding'].apply(lambda x: cosine_similarity(x, pregunta_embed))
    datos = datos.sort_values("Similitud", ascending=False)
    # Obtener los datos de los primeros 5 elementos de la columna "texto" en una lista
    lst_respuestas = datos.iloc[:n_resultados][["texto"]]
    txt_respuesta = responder_la_pregunta(txt_pregunta, lst_respuestas)
    
    dict_respuesta = {
            'Respuesta': txt_respuesta
            }

    return dict_respuesta



if __name__ == "__main__":
    
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
   
    txt_pregunta = input("Ingrese la pregunta (Enter para usar 'Salir'): ") or 'Salir'
    if txt_pregunta != "Salir":
        print(f"Buscando las respuestas...")

        embeddings_pkl = configuracion["arch_bin"]["path_arch_bin"] +  configuracion["arch_bin"]["embed_pkl"]
        n_resultados = configuracion["preg_resp"]["n_resultados"]
        m_logging.msg_logging(f'La pregunta es: {txt_pregunta} El archivo de embeddings es: {embeddings_pkl}\n El número de resultados es: {n_resultados}')
        txt_respuesta = pregunta_y_respuesta(txt_pregunta, embeddings_pkl, n_resultados)
        m_logging.msg_logging(f'La respuesta es: {txt_respuesta}')
        print("Respuesta:", txt_respuesta)