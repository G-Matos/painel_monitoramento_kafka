from request import get_status_sink , get_status_source
from datetime import datetime, date

class LogWrite():

    log_path = "logs/"

    def http_log():
        return

    def panel_log():
        return

""" 
def log_write():
    sink_info = pd.DataFrame(get_status_sink())
    source_info = pd.DataFrame(get_status_source())
    concat_df = pd.concat([sink_info, source_info])
    log_paused_df = concat_df[concat_df["Status Atual"] == "PAUSED"]
    log_failed_df = concat_df[concat_df["Status Atual"] == "FAILED"]
    current_time = datetime.now()
    current_date = date.today()
    formatted_date = current_date.strftime("%Y-%m-%d")
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")

    if not log_paused_df.empty:
        for row in log_paused_df.values:
            with open(f"logs/log_{formatted_date}.txt", "a") as log_file:
                log_file.write(f"{formatted_time} - [INFO] - {row}\n")
    elif not log_failed_df.empty:
        for rec in log_failed_df.values:
            with open(f"logs/log_{formatted_date}.txt", "a") as log_file:
                log_file.write(f"{formatted_time} - [INFO] [FAILED] - {rec}\n")         

"""