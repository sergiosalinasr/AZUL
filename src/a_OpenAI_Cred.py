
from openai import OpenAI
import os

def credenciales_openai():
    #subir el archivo JSON cfg.py que contiene la API KEY
    import cfg as cfg
    OPENAI_API_KEY = cfg.api_key["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    print(OPENAI_API_KEY)
    #openai.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
    )