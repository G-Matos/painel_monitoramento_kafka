import sqlite3
from config import * 

# conexão DB
def sql_info():
    dbcon = sqlite3.connect(db_path)
    cur = dbcon.cursor()
    cur.execute("select licenca, ip, porta FROM ConnectorsTab")
    resultTB = cur.fetchall()
    return resultTB