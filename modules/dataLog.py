from datetime import datetime, date

class LogWrite:

    log_path = "sysfiles/logs/"

    def __init__(self, log_path=None):

        if log_path:
            self.log_path = log_path

    def log_write(self, log_info, log_type):

        current_time = datetime.now()
        current_date = date.today()
        formatted_date = current_date.strftime("%Y-%m-%d")
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")

        log_file_path = f"{self.log_path}log_{formatted_date}.txt"

        for val in log_info:
            with open(log_file_path, "a") as log_file:
                if log_type == "paused":
                    log_file.write(f"{formatted_time} - [INFO] - {val}\n")
                elif log_type == "failed":
                    log_file.write(f"{formatted_time} - [INFO] [FAILED] - {val}\n")
                elif log_type == "error":
                    log_file.write(f"{formatted_time} - [INFO] [ERROR] - {val}\n")
    
