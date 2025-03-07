import pandas as pd
import requests, json
from config import kafka_ip

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
class Requests():

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
            return str(exc)
    
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
                url = Requests.set_url(port, connector)
                response = Requests.http_req(url)
                if response:
                    conector = response['name']
                    status_anterior = response['connector']['state']
                    status_atual = response['tasks'][0]['state']
                    porta_kafka = response['connector']['worker_id'].split(":")[-1] 
                    trace = response.get("tasks", [{}])[0].get("trace", "N/A")
                    error_msg = response.get("error_msg", "")
                    c_type = response['type']
                    
                    if trace != "N/A":
                        match = re.search(r'Caused by: (.*?)(.{1,200})', trace)
                        trace_message = match.group(1).strip() if match else "N/A"
                    elif error_msg:
                        mensagem = error_msg
                    else:
                        trace_message = "N/A"
                        mensagem = trace_message

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


