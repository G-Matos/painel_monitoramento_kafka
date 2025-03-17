import pandas as pd
import requests, json, re
from modules.config import kafka_ip

# obtem informações dos conectores 
class SetConnector():

    @staticmethod
    def get_connector(kafka_ports):
        connectors = {}

        for rec in kafka_ports:
            try:
                response = requests.get(f"http://{kafka_ip}:{rec}/connectors/")
                if response.status_code == 200:
                    connectors[rec] = response.json()
                else:
                    connectors[rec] = f"Erro: {response.status_code}"
            except requests.exceptions.RequestException as e:
                connectors[rec] = f"Erro na requisição: {e}"

        resultado = {}

        for port, connectors_list in connectors.items():
            resultado[str(port)] = {
                "Connectors": connectors_list
            }

        # salva os dados em arquivo Json
        with open('sysfiles/data.json', 'w') as f:
            json.dump(resultado, f, indent=4)

        return resultado

# requisições http
class HttpRequests():

    # set url 
    @staticmethod
    def set_url(port, connector):

        url = f"http://{kafka_ip}:{port}/connectors/{connector}/status"
        return url

    # realiza requisição
    @staticmethod
    def http_req(url):

        try:
            req = requests.get(url)
            if req.status_code == 200:
                return json.loads(req.content)
            else:
                return f"Erro: Status code {req.status_code}"
        except Exception as exc:
            error_msg = {
                    'name': 'N/A',
                    'connector': {'state':'N/A','worker_id': 'N/A'},
                    'tasks': [{'id': 0, 'state': 'N/A', 'worker_id': 'N/A'}],
                    'type': 'sink',
                    'error_msg': str(exc)
                }
            return error_msg

    # obtem a informação do Json e realiza a requisição (retorno dos dados )
    @staticmethod   
    def connector_info():

        kafka_info = []

        with open('sysfiles/data.json', 'r') as json_data:
            dados = json.load(json_data)

        ports = list(dados.keys())

        connectors = {}

        for port, data in dados.items():
            connectors[port] = data["Connectors"]

        for port in ports:
            for connector in connectors[port]:
                url = HttpRequests.set_url(port, connector)
                response = HttpRequests.http_req(url)
                if response:
                    conector = response['name']
                    status_anterior = response['connector']['state']
                    status_atual = response['tasks'][0]['state']
                    porta_kafka = response['connector']['worker_id'].split(":")[-1] 
                    trace = response.get("tasks", [{}])[0].get("trace", "N/A")
                    error_msg = response.get("error_msg", "")
                    c_type = response['type']
                    
                    if trace != "N/A":
                        match_dbmaker = re.search(r'(?<=Caused by.)(.*)', trace)
                        match_kafka = re.search(r'(?<=org\.apache\.kafka\.connect\.errors\.)(.*)', trace)
                        if match_dbmaker:
                            mensagem = match_dbmaker.group(1).strip() if match_dbmaker else "N/A"
                        elif match_kafka:
                            mensagem = match_kafka.group(1).strip() if match_kafka else "N/A"
                    elif error_msg:
                        mensagem = error_msg
                    else:
                        mensagem = trace

                    kafka_info.append({
                        "Conector": conector, 
                        "Status Anterior": status_anterior, 
                        "Status Atual": status_atual,
                        "Porta": porta_kafka,
                        "Type": c_type,
                        "Mensagem": mensagem
                    })

                    status_df = pd.DataFrame(kafka_info)

        return status_df


