import pytest
from flask import Flask, jsonify
import json
from m_crawler import Crawler, crawl

def test_download_url():
    crawler = Crawler()
    url = "https://www.example.com"
    expected_text = "<!doctype html>"
    result = crawler.download_url(url)
    
    assert expected_text in result, f'El texto esperado no está presente en la respuesta. Respuesta actual: {result}'

@pytest.mark.parametrize(
    "url, expected_text",
    [
        ("https://www.example.com", "<!doctype html>")
    ]
)
def test_download_url_parametrized(url, expected_text):
    crawler = Crawler()
    result = crawler.download_url(url)
    
    assert expected_text in result, f'El texto esperado no está presente en la respuesta. Respuesta actual: {result}'

#Prueba de crawler
#["texto", " This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission. More information..."]

@pytest.mark.parametrize(
    "webpage, unaPagina_UnTexto, lista_esperada",
    [
        ("https://www.example.com", True, {'lista_meta': [{'web_page': 'https://www.example.com'}, {'unaPagina_UnTexto': True}, {'nombre_archivo': './datos/textos.csv'}], 'lista_valores': [{'clave': 'clave0', 'valor': 'texto'}, {'clave': 'clave1', 'valor': 'This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.'}, {'clave': 'clave2', 'valor': 'More information...'}]})
    ]
)
def test_crawl_parametrized(webpage, unaPagina_UnTexto, lista_esperada):
    
    dict_resultado = crawl(webpage, unaPagina_UnTexto)
    print("dict_resultado:")
    valor_resultado = dict_resultado['lista_valores'][1]['valor']
    print("lista_esperada:")
    valor_esperado = lista_esperada['lista_valores'][1]['valor']
    #json_lista_esperada = jsonify(lista_esperada)
    
    assert valor_esperado == valor_resultado