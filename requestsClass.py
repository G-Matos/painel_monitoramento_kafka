import pandas as pd
import json, sqlite3, requests, re
from config import *

""" 
f"http://144.22.196.245:15005/connectors/2801-sink-jcontrol/status"
f"http://144.22.196.245:26005/connectors/2801-source-jcontrol/status"
"""
# classe reqsuisicoes http
class Requests():
    
    # conexão DB
    def sql_info():
        dbcon = sqlite3.connect(db_path)
        cur = dbcon.cursor()
        cur.execute("select licenca, ip, porta FROM ConnectorsTab")
        resultTB = cur.fetchall()
        return resultTB

    # metodos
    def req_connector(httpGet):
        try:
            r = requests.get(httpGet)
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

class GetConnector():

    #sink_url = f"http://{sink_address}/connectors/{licenca}-sink-jcontrol/status"
    #source_url = f"http://{ip_kafka}:{PortaTB}/connectors/{licenca}-source-jcontrol/status"

    # lista de conectores
    def http_get(ip_addres):
        connector_name = []
        connectors = Requests.req_connector(f"http://{ip_addres}/connectors")
        for items in connectors:   
            connector_name.append(items)
        return connector_name



