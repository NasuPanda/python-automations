from config import helper

# Load config yaml.
CONFIG_YAML_PATH = "./config.yml"
config_data = helper.load_yaml(CONFIG_YAML_PATH)

MONITOR_INTERVAL_MINUTES = config_data["monitor_interval_minutes"]
LOG_FOLDER = config_data["log_folder"]
FACILITY_NAME = config_data["facility_name"]
CSV_COLUMNS = config_data["csv_columns"]
# Log file path
log_file_name = helper.log_file_name(attached_string=FACILITY_NAME, extension=".csv")
log_file_name_resolved_conflict = helper.resolve_filename_conflict(log_file_name, LOG_FOLDER)
LOG_FILE_PATH = helper.log_file_path(LOG_FOLDER, log_file_name_resolved_conflict)
