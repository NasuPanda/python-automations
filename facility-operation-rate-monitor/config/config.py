from config import helper


LOG_FOLDER = "./test/fixtures/duplication_exist"
FACILITY_NAME = "facility_A"
log_file_name = helper.log_file_name(FACILITY_NAME)
log_file_name_resolved_conflict = helper.resolve_filename_conflict(log_file_name, LOG_FOLDER)
LOG_FILE_PATH = helper.log_file_path(LOG_FOLDER, log_file_name)
