import pandas as pd
import json, sqlite3, requests, re
from config import *

# classe reqsuisicoes http
class Requests():

    def http_req(url):
        try:
            req = requests.get(url)
            if req.status_code == 200:
                return json.loads(req.content)
        except Exception as exc:
            return exc

class SetUrl():

    def set_url(port, connector):
        url = f"http://144.22.196.245:{port}/connectors/{connector}/status"
        return url

# obten todos os conectores em arquivo
def list_conn():
    for rec in kafka_ports:
        response = Requests.http_req(f"http://144.22.196.245:{rec}/connectors/")

        # Se a resposta for uma lista, iteramos corretamente
        if isinstance(response, list):
            with open("logs/list_conn.txt", "a") as file:  # 'a' para não sobrescrever
                for item in response:
                    file.write(f"{item}\n")  # Adiciona quebra de linha
