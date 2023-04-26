from config import helper

LOCK_TASK_BAT_FILE = r"..\..\bat\stop.bat"
UNLOCK_TASK_BAT_FILE = r".\..\bat\exec_vbs_wrapper.bat"
CURRENT_PID_FILE = r"../../temp/current_pid"
CONFIG_YAML_PATH: str = r"..\..\config.yml"

# Load config yaml.
config_data = helper.load_yaml(CONFIG_YAML_PATH)

MONITOR_INTERVAL_MINUTES: int = config_data["monitor_interval_minutes"]
SLEEP_TIME: int = config_data["sleep_time"]
FACILITY_NAME: str = config_data["facility_name"]
MONITORING_PROCESSES: list = config_data["monitoring_process"]["names"]
CSV_COLUMNS: dict = config_data["csv_columns"]

# Set log file path
LOG_FOLDER: str = config_data["log_folder"]
log_file_name = helper.log_file_name(attached_string=FACILITY_NAME, extension=".csv")
LOG_FILE_PATH: str = helper.log_file_fullpath(LOG_FOLDER, log_file_name)
