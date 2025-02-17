import pandas as pd
import json, sqlite3, requests, re
from config import ip_porta , source_ip, db_path

def req_connector(url, connector_name = ""):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return json.loads(r.content)
    except Exception as exc:
        error_msg = {
                'name': 'N/A',
                'connector': {'state':'N/A','worker_id': 'N/A'},
                'tasks': [{'id': 0, 'state': 'N/A', 'worker_id': 'N/A'}],
                'type': 'sink',
                'error_msg': str(exc)
            }

        return error_msg

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
        get_sink = req_connector(f"http://{ip_porta}/connectors/{connector}/status", connector)
        if get_sink:
            conector = get_sink['name']
            status_anterior = get_sink['connector']['state']
            status_atual = get_sink['tasks'][0]['state']
            porta_kafka = get_sink['connector']['worker_id'].split(":")[-1] 
            trace = get_sink.get("tasks", [{}])[0].get("trace", "N/A")
            error_msg = get_sink.get("error_msg", "")

            if trace != "N/A":
                match = re.search(r'Caused by: (.*?)(.{1,200})', trace)
                trace_message = match.group(1).strip() if match else "N/A"
            elif error_msg:
                mensagem = error_msg
            else:
                trace_message = "N/A"
                mensagem = trace_message

            sink_info.append({
                "Conector": conector, 
                "Status Anterior": status_anterior, 
                "Status Atual": status_atual,
                "Porta": porta_kafka,
                "Mensagem": mensagem
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
        get_source = req_connector(f'http://{source_ip}:{PortaTB}/connectors/{LicencaTB}-source-jcontrol/status', connector_name = f"{LicencaTB}-source-jcontrol")
        if get_source:
            conector = get_source['name']
            status_anterior = get_source['connector']['state']
            status_atual = get_source['tasks'][0]['state']
            porta_kafka = get_source['connector']['worker_id'].split(":")[-1]
            error_msg = get_source.get("error_msg", "")
            
            trace = get_source.get("tasks", [{}])[0].get("trace", "N/A")
            if trace != "N/A":
                match = re.search(r'Caused by: (.*?)(.{1,200})', trace)
                trace_message = match.group(1).strip() if match else "N/A"
            elif error_msg:
                mensagem = error_msg
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



