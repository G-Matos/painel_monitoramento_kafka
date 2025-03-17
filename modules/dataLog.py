from modules.requestsClass import *
from datetime import datetime, date

class LogWrite():

    log_path = "logs/"

    def http_log(log_info, log_type):
        current_time = datetime.now()
        current_date = date.today()
        formatted_date = current_date.strftime("%Y-%m-%d")
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")

        if log_type == "paused":
            for row in log_info:
                with open(f"sysfiles/logs/log_{formatted_date}.txt", "a") as log_file:
                    log_file.write(f"{formatted_time} - [INFO] - {row}\n")
        elif log_type == "failed":
            for row in log_info:
                with open(f"sysfiles/logs/log_{formatted_date}.txt", "a") as log_file:
                    log_file.write(f"{formatted_time} - [INFO] [FAILED] - {row}\n")
        elif log_type == "error":
            for row in log_info:
                with open(f"sysfiles/logs/log_{formatted_date}.txt", "a") as log_file:
                    log_file.write(f"{formatted_time} - [INFO] [ERROR] - {row}\n")

    def panel_log():
        return
