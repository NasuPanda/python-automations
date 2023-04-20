from config import helper
from utils.exceptions import ArrayLengthNotMatchError


CURRENT_PID_FILE = r"./temp/current_pid"
# Load config yaml.
CONFIG_YAML_PATH: str = r"./config.yml"
config_data = helper.load_yaml(CONFIG_YAML_PATH)

MONITOR_INTERVAL_MINUTES: int = config_data["monitor_interval_minutes"]
SLEEP_TIME: int = config_data["sleep_time"]
FACILITY_NAME: str = config_data["facility_name"]

MONITORED_PROCESSES: list[str] | None = config_data["monitored_processes"]["names"]
CPU_USAGE_THRESHOLDS: list[float] | None = config_data["monitored_processes"]["cpu_usage_thresholds"]

if MONITORED_PROCESSES and CPU_USAGE_THRESHOLDS:
    if len(MONITORED_PROCESSES) != len(CPU_USAGE_THRESHOLDS):
        raise ArrayLengthNotMatchError(f"{MONITORED_PROCESSES} and {CPU_USAGE_THRESHOLDS} length are not match.")

CSV_COLUMNS: dict[str, str] = config_data["csv_columns"]
# Set log file path
LOG_FOLDER: str = config_data["log_folder"]
log_file_name = helper.log_file_name(attached_string=FACILITY_NAME, extension=".csv")
LOG_FILE_PATH: str = helper.log_file_fullpath(LOG_FOLDER, log_file_name)
