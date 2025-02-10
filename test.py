import pandas as pd
import requests, re, json

def req_connector(url):
    error_msg = {}
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return json.loads(r.content)
    except Exception as exc:
        error_msg = {
            "name": "0000-sink-jcontrol",
            "connector": {"state": "N/A", "worker_id": "N/A"},
            "tasks": [{"id": 0, "state": "N/A", "worker_id": "N/A"}],
            "type": "sink",
            "error_msg": exc
        }
        return error_msg
    
def test_func():
    sink_info = []
    get_sink = req_connector(f"http://144.22.196.245:15001/connectors/2016-sink-jcontrol/status")
    if get_sink:
            conector = get_sink["name"]
            status_anterior = get_sink["connector"]["state"]
            status_atual = get_sink["tasks"][0]["state"]
            porta_kafka = get_sink["connector"]["worker_id"].split(":")[-1] 
            trace = get_sink.get("tasks", [{}])[0].get("trace", "N/A")
            error_msg = get_sink["error_msg"]

            if trace != "N/A":
                match = re.search(r'org\.apache\.kafka\.connect\.errors\.(.*?)(,|\n)', trace)
                trace_message = match.group(1).strip() if match else "N/A"
            elif error_msg != "N/A":
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

def test_name():
    connector_name = []
    name_command = req_connector(f"http://144.22.196.245:15005/connectors")
    print(name_command)

#print(req_connector(f"http://144.22.196.245:15001/connectors/2016-sink-jcontrol/status"))
test = test_func()
print(test)