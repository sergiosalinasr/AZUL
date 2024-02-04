from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

import m_crawler
import m_embed_text
import m_resp_pregunta
import m_auth

import inspect
#import logging
import m_logging
import m_carga_config

app = Flask(__name__)
# Habilita CORS para toda la aplicación, lo cual es útil para el desarrollo.
# Para producción, es mejor especificar los orígenes permitidos.
CORS(app)

# Tus rutas y lógica de la aplicación aquí

configuracion = m_carga_config.cargar_configuracion()

m_carga_config.carpetas_base()

# Testing Route
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

@app.route('/health', methods=['GET'])
def health():
    #logging.info(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    
    return jsonify({'response': 'Healthy'})

@app.route('/crawl', methods=['POST'])
def crawl():
    #logging.info(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    print(request.json)
    unaPagina_UnTexto = request.json['unaPagina_UnTexto']   
    web_page = request.json['web_page']
    print(f'crawl parametros: {web_page, unaPagina_UnTexto}')
    dic_respuesta = m_crawler.crawl(web_page, unaPagina_UnTexto)
    return jsonify(dic_respuesta)
    #return jsnfy_respuesta

@app.route('/embed_text', methods=['POST'])
def embed_text():
    #logging.info(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    print(request.json)

    textos_csv = request.json['textos_csv']

    dict_respuesta = m_embed_text.embed_text(textos_csv)

    return jsonify(dict_respuesta)

@app.route('/resp_pregunta', methods=['POST'])
def resp_pregunta():
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    print(request.json)

    txt_pregunta = request.json['txt_pregunta']
    embeddings_pkl = request.json['embeddings_pkl']
    n_resultados = request.json['n_resultados']

    dict_respuesta = m_resp_pregunta.pregunta_y_respuesta(txt_pregunta, embeddings_pkl, n_resultados)

    return jsonify(dict_respuesta)

# Esta endpint es para colaborar en la aplicación Angular "pacientes", que necesita un auth
@app.route('/auth', methods=['POST'])
def auth():
    
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    print(request.json)

    usuario = request.json['usuario']
    password = request.json['password']

    dict_respuesta = m_auth.auth(usuario, password)

    return jsonify(dict_respuesta)

if __name__ == '__main__':
        app.run(host="0.0.0.0",debug=True, port=4000)
