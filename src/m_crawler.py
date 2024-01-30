
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from unidecode import unidecode
import csv
#import logging
import json
import re
import inspect
from flask import Flask, jsonify, request
import m_logging
import m_guardar_json
import m_carga_config

configuracion = m_carga_config.cargar_configuracion()

class Crawler:

    def __init__(self, urls=[]):
        
        #logging.info(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
        m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
        self.visited_urls = []
        self.urls_to_visit = urls
        self.unaPagina_unTexto = True # Permite controlar que todos los parrafos de una página los considere como uno solo
        self.numMinCaracteres = 4 # Permite controlar la cantidad
        self.webpageorigen = ""

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            url_string = str(url)
            if url_string.startswith(self.webpageorigen):
                self.add_url_to_visit(url)

    def quitarPaginasRepetidas(self):
        result_aux = []
        for item in self.visited_urls:
            texto = item
            if texto.endswith('/'):
                texto = texto[:-1]
            if texto not in result_aux:
                result_aux.append(texto)
        return result_aux
    
    def limpiar_texto(self, texto):
        # Cambiar las letras acentuadas por sus equivalentes sin acento
        # pedir input para una pausa
        #input("Texto ANTES de unicode:" + texto)
        texto_corregido = texto.replace("Ã¡", "a").replace("Ã©", "e").replace("Ã­", "i").replace("Ã³", "o").replace("Ãº", "u").replace("Ã±", "n") #Ã±

        texto_limpio = unidecode(texto_corregido)
        #input("Texto DESPUES" + texto_limpio)
        
        # Cambiar caracteres que no son letras o números por un espacio en blanco
        texto_limpio = re.sub(r'[^a-zA-Z0-9 \(\)\.]', ' ', texto_limpio)
        
        # Cambiar espacios en blanco múltiples por uno solo
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
        
        return texto_limpio

    def textosDeLaPagina(self, url):
        #Diccionario de textos de la pagina web
        lista_textos = []
        dic_textos = {}
        
        # Realiza una solicitud GET para obtener el contenido de la página
        response = requests.get(url)
        
        # Comprueba si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Parsea el contenido HTML de la página con BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
        
            # Encuentra todos los párrafos en la página
            elements_to_find = ['p', 'h2', 'h3', 'H3', 'otros_elementos']  # Agrega aquí los elementos que deseas buscar
        
            #found_elements = soup.find_all(elements_to_find)
            paragraphs = soup.find_all(elements_to_find)
        
            # Itera a través de los párrafos e imprímelos
            for paragraph in paragraphs:
                #texto_limpio = self.limpiar_cadena(paragraph.text.replace('\n', ''))
                texto_limpio = self.limpiar_texto(paragraph.text.replace('\n', ''))
                if len(texto_limpio) > self.numMinCaracteres:
                    dic_textos = { 'texto': paragraph.text.replace('\n', '') }
                    if texto_limpio not in lista_textos:
                        lista_textos.append( texto_limpio)                
        
        return lista_textos

    def lista2csv(self, lista_textos, archivo_csv):
        """
        Escribe una lista de textos en un archivo CSV.
        :param lista_textos: Lista de textos a escribir en el archivo CSV
        :param nombre_archivo: Nombre del archivo CSV
        """
        # Abrir el archivo CSV para escritura
        with open(archivo_csv, mode='w', newline='', encoding="utf-8") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            
            # Escribir la lista en el archivo CSV
            for texto in lista_textos:
                escritor_csv.writerow([texto])

    #Toma una lista de textos y los une en un solo texto
    def unir_textos(self, lista_textos):
        texto_unido = ""
        for texto in lista_textos:
            texto_unido = texto_unido + " " + texto
        return texto_unido


    def run(self, unaPagina_UnTexto, webpage):
        #logging.info(f'run parametros: {unaPagina_UnTexto}')
        self.unaPagina_unTexto = unaPagina_UnTexto
        self.webpageorigen = webpage
        result = []
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            #logging.info(f'Crawling: {url}')
            m_logging.msg_logging(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                #logging.exception(f'Failed to crawl: {url}')
                m_logging.msg_logging(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)
                    
        # quitar las páginas repetidas de la lista de páginas visitadas
        result = self.quitarPaginasRepetidas()
        
        lista_textos_p = []
        lista_textos = ["texto"]
        #por cada elemento de la lista de páginas visitadas, obtener los textos
        for pagina in result:
            print("Obteniendo textos de la página:", pagina)
            lista_textos_p = self.textosDeLaPagina(pagina)
            #if self.unaPagina_unTexto:
            #    lista_textos.append(self.unir_textos(lista_textos_p))
            #else:
            for texto in lista_textos_p:
                if texto not in lista_textos:
                            lista_textos.append( texto) 
        
        return lista_textos
            

def crawl(web_page, unaPagina_UnTexto):
    #m_logging.m_logging()
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    #web_page = 'https://azurian.com/'
    #https://www.emol.com/especiales/2023/nacional/proceso-constitucional/propuesta-constitucion.asp
    #logging.info(f'crawl parametros: {web_page, unaPagina_UnTexto}')
    result = []
    try:
        request = requests.get(web_page, timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        print("Sin conexión a la página o la página no existe:", web_page)
        #Retora un JSON vacío
        return json.dumps({'response': 'La página no responde'})

    else:
        
        print(f'Crawling: Inicio de la búsqueda con: {web_page}')
        result = Crawler(urls=[web_page]).run(unaPagina_UnTexto, web_page)

        # Nombre del archivo CSV
        nombre_archivo = configuracion["craw"]["path_arch_csv"] +  configuracion["craw"]["textos_csv"]
        
        Crawler.lista2csv(Crawler, result, nombre_archivo)

        # Usar claves fijas
        #lista_diccionarios = [{'clave': f'clave{i}', 'valor': valor} for i, valor in enumerate(result)]
        lista_diccionarios2 = {
            'lista_meta': [{'web_page': web_page},
            {'unaPagina_UnTexto': unaPagina_UnTexto},
            {'nombre_archivo': nombre_archivo}],
            'lista_valores': [{'clave': f'clave{i}', 'valor': valor} for i, valor in enumerate(result)]
        }

        # Guardar el diccionario en un archivo JSON
        textos_json = configuracion["craw"]["textos_json"]
        m_guardar_json.m_guardar_json(lista_diccionarios2, textos_json)
        
        print("Fin de la búsqueda.")

        return lista_diccionarios2
    


    # Programa principal

if __name__ == "__main__":
    #logging.info(f'__main__')
    m_logging.msg_logging(f'__main__')
    print("Aplicación de Ejemplo")
    #logging.info(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
    m_logging.msg_logging(f'M: {inspect.getmodulename(__file__)} F: {inspect.currentframe().f_code.co_name}')
   
    web_page = input("Ingresar la webpage (o presiona Enter para usar 'https://www.example.com/'): ") or 'https://www.example.com/'
    #web_page = input("Ingresar la webpage para hacer el crawler (https://azurian.com/): ")
    #logging.info(f'Main, pagina a examinar: {web_page}')
    Pregunta_unaPagina_UnTexto = input("Una página, un texto? 'S'): ") or 'S'
    #logging.info(f'Main, Pregunta_unaPagina_UnTexto: {Pregunta_unaPagina_UnTexto}')
    m_logging.msg_logging(f'Main, Pregunta_unaPagina_UnTexto: {Pregunta_unaPagina_UnTexto}')
    if Pregunta_unaPagina_UnTexto == 'S':
        unaPagina_UnTexto = True
    else:
        unaPagina_UnTexto = False
    print(crawl(web_page, unaPagina_UnTexto))