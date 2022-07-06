from config import helper


LOG_FOLDER = "./logs"
FACILITY_NAME = "facility_A"
log_file_name = helper.log_file_name(FACILITY_NAME)
LOG_FILE_PATH = helper.log_file_path(LOG_FOLDER, log_file_name)
