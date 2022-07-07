from config import helper

# Load config yaml.
CONFIG_YAML_PATH: str = "./config.yml"
config_data = helper.load_yaml(CONFIG_YAML_PATH)

MONITOR_INTERVAL_MINUTES: int = config_data["monitor_interval_minutes"]
FACILITY_NAME: str = config_data["facility_name"]
MONITORED_PROCESSES: list[str] | None = config_data["monitored_processes"]
CSV_COLUMNS: dict[str, str] = config_data["csv_columns"]
# Set log file path
LOG_FOLDER: str = config_data["log_folder"]
log_file_name = helper.log_file_name(attached_string=FACILITY_NAME, extension=".csv")
LOG_FILE_PATH: str = helper.log_file_fullpath(LOG_FOLDER, log_file_name)
