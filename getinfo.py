import pandas as pd
import subprocess
import re
import json
import sqlite3
from config import ip_porta , source_ip, db_path

# global variables
#dbcon = sqlite3.connect("dbPython.db")
log_message_source = []

def get_connector_name():
    connector_name = []
    name_command = f"curl -s http://{ip_porta}/connectors"
    run_name_command = subprocess.run(name_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True, shell=True)
    result_name_command = run_name_command.stdout
    matches = re.findall(r'"(.*?)"', result_name_command)
    for items in matches:   
        connector_name.append(items)
    return connector_name

# sink connector
def get_status_sink():
    log_messages_sink = []
    sink_info = []
    for name in get_connector_name():
        status_command = f"curl -s http://{ip_porta}/connectors/{name}/status | jq"
        run_status_command= subprocess.run(status_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        result_status_command = run_status_command.stdout
        
        if result_status_command:
            try:
                response_json = json.loads(result_status_command)
                conn_name = response_json.get("name", "N/A")
                status_anterior = response_json.get("connector", {}).get("state", "N/A")
                status_atual = (response_json.get("tasks",[{}])[0].get("state", "N/A"))
                worker_id = response_json.get("connector", {}).get("worker_id", "N/A")
                worker_id_last_5 = worker_id[-5:] if worker_id != "N/A" else "N/A"

                trace = response_json.get("tasks", [{}])[0].get("trace", "N/A")
                if trace != "N/A":
                    match = re.search(r'org\.apache\.kafka\.connect\.errors\.(.*?)(,|\n)', trace)
                    trace_message = match.group(1).strip() if match else "N/A"
                else:
                    trace_message = "N/A"
                
                sink_info.append({
                    "Conector": conn_name,
                    "Status Anterior": status_anterior,
                    "Status Atual": status_atual,
                    "Porta Kafka": worker_id_last_5,
                    "Mensagem": trace_message
                })
        
            except json.JSONDecodeError:
                error_message = f"Erro ao decodificar Json da licença {conn_name}"
                log_messages_sink.append(error_message)
            else:
                error_message = f"Sem retorno do comando curl para os conectores na porta {ip_porta}."

    return pd.DataFrame(sink_info), log_messages_sink

# Source Connector
def get_status_source():
    dbcon = sqlite3.connect(db_path)
    cur = dbcon.cursor()
    cur.execute("select licenca, porta FROM ConnectorsTab")
    resultTB = cur.fetchall()
    source_info = []
    #for name in get_connector_name():
    #    status_command = f"curl -s http://{ip_porta}/connectors/{name}/status | jq"
    #    run_status_command = subprocess.run(status_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    for LicencaTB, PortaTB in resultTB:

        curlCommand = f"curl http://{source_ip}:{PortaTB}/connectors/{LicencaTB}-source-jcontrol/status | jq"
        try:

            runCommand = subprocess.run(curlCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            returnCommand = runCommand.stdout.strip()
            
            if returnCommand:

                try:
                    response_json = json.loads(returnCommand)
                    name = response_json.get("name", "N/A")
                    status_anterior = response_json.get("connector", {}).get("state", "N/A")
                    status_atual = (response_json.get("tasks", [{}])[0].get("state", "N/A"))
                    worker_id = response_json.get("connector", {}).get("worker_id", "N/A")
                    worker_id_last_5 = worker_id[-5:] if worker_id != "N/A" else "N/A"
                    
                    trace = response_json.get("tasks", [{}])[0].get("trace", "N/A")
                    if trace != "N/A":
                        match = re.search(r'org\.apache\.kafka\.connect\.errors\.(.*?)(,|\n)', trace)
                        trace_message = match.group(1).strip() if match else "N/A"
                    else:
                        trace_message = "N/A"

                    source_info.append({
                        "Conector": name,
                        "Status Anterior": status_anterior,
                        "Status Atual": status_atual,
                        "Porta Kafka": worker_id_last_5,
                        "Mensagem": trace_message
                    })

                except json.JSONDecodeError:
                    error_message = f"Erro ao decodificar JSON para Licença {LicencaTB} e Porta {PortaTB}."
                    log_message_source.append(error_message)
        
            else:
                no_response_message = f"Sem retorno do comando curl para Licença {LicencaTB} e Porta {PortaTB}."
                log_message_source.append(no_response_message)
 
        except Exception as e:
            exception_message = f"Erro ao executar o comando para Licença {LicencaTB} e Porta {PortaTB}: {e}"
            log_message_source.append(exception_message)

    return pd.DataFrame(source_info) , log_message_source
