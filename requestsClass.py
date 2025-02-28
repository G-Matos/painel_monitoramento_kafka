import pandas as pd
import requests, re, json
from config import *

# Classe para obter URLs
class SetUrl():

    @staticmethod
    def get_connector(kafka_ports):
        connectors = {}

        for rec in kafka_ports:
            try:
                response = requests.get(f"http://144.22.196.245:{rec}/connectors/")
                if response.status_code == 200:
                    connectors[rec] = response.json()
                else:
                    connectors[rec] = f"Erro: {response.status_code}"
            except requests.exceptions.RequestException as e:
                connectors[rec] = f"Erro na requisição: {e}"

        resultado = {}

        # Organizando os dados
        for port, connectors_list in connectors.items():
            resultado[str(port)] = {
                "Connectors": connectors_list
            }

        # Salvando os dados no arquivo JSON
        with open('sysfiles/data.json', 'w') as f:
            json.dump(resultado, f, indent=4)

        return resultado

# Classe para requisições HTTP
class Requests():

    @staticmethod
    def set_url(port, connector):
        # Gerando a URL
        url = f"http://144.22.196.245:{port}/connectors/{connector}/status"
        return url

    @staticmethod
    def http_req(url):
        # Realizando a requisição HTTP
        try:
            req = requests.get(url)
            if req.status_code == 200:
                return json.loads(req.content)
            else:
                return f"Erro: Status code {req.status_code}"
        except Exception as exc:
            return str(exc)
        
    @staticmethod   
    def connector_info():
        # Lendo os dados do arquivo JSON
        with open('sysfiles/data.json', 'r') as f:
            dados = json.load(f)

        ports = list(dados.keys())
        connectors = {}

        # Organizando os conectores para cada porta
        for port, data in dados.items():
            connectors[port] = data["Connectors"]

        # Iterando sobre as portas e conectores para acionar as funções
        for port in ports:
            for connector in connectors[port]:
                # Gerando a URL para cada conector
                url = Requests.set_url(port, connector)

                # Chamando a função http_req e imprimindo a resposta
                response = Requests.http_req(url)
                return response