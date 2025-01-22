import pandas as pd
import json
import sqlite3
import requests
from config import ip_porta , source_ip, db_path
import re

log_message_source = []

def req_connector(url):
    r = requests.get(url)
    if r.status_code == 200:
        try:
            return json.loads(r.content)
        except Exception as exc:
            raise RuntimeError("Erro na requisição!") from exc

def get_connector_name():
    connector_name = []
    name_command = req_connector(f"http://{ip_porta}/connectors")
    for items in name_command:   
        connector_name.append(items)
    return connector_name

# sink connector
def get_status_sink():
    sink_info = []
    for connector in get_connector_name():
        get_sink = req_connector(f"http://{ip_porta}/connectors/{connector}/status")
        if get_sink:
            conector = get_sink['name']
            status_anterior = get_sink['connector']['state']
            status_atual = get_sink['tasks'][0]['state']
            porta_kafka = get_sink['connector']['worker_id'].split(":")[-1]

            trace = get_sink.get("tasks", [{}])[0].get("trace", "N/A")
            if trace != "N/A":
                match = re.search(r'org\.apache\.kafka\.connect\.errors\.(.*?)(,|\n)', trace)
                trace_message = match.group(1).strip() if match else "N/A"
            else:
                trace_message = "N/A"
            mensagem = trace_message

            sink_info.append({
                "Conector": conector, 
                "Status Anterior": status_anterior, 
                "Status Atual": status_atual,
                "Porta": porta_kafka,
                "Mensagem":mensagem
            })
            
            sink_df = pd.DataFrame(sink_info)

    return sink_df

def get_status_source():
    dbcon = sqlite3.connect(db_path)
    cur = dbcon.cursor()
    cur.execute("select licenca, porta FROM ConnectorsTab")
    resultTB = cur.fetchall()
    source_info = []
    for LicencaTB, PortaTB in resultTB:
        get_source = req_connector(f'http://{source_ip}:{PortaTB}/connectors/{LicencaTB}-source-jcontrol/status')
        if get_source:
                conector = get_source['name']
                status_anterior = get_source['connector']['state']
                status_atual = get_source['tasks'][0]['state']
                porta_kafka = get_source['connector']['worker_id'].split(":")[-1]

                trace = get_source.get("tasks", [{}])[0].get("trace", "N/A")
                if trace != "N/A":
                    match = re.search(r'org\.apache\.kafka\.connect\.errors\.(.*?)(,|\n)', trace)
                    trace_message = match.group(1).strip() if match else "N/A"
                else:
                    trace_message = "N/A"
                mensagem = trace_message
                
                source_info.append({
                    "Conector": conector, 
                    "Status Anterior": status_anterior, 
                    "Status Atual": status_atual,
                    "Porta": porta_kafka,
                    "Mensagem":mensagem
                })
        
                source_df = pd.DataFrame(source_info)

    return source_df

if __name__ == "__main__":
    print(get_status_source())


