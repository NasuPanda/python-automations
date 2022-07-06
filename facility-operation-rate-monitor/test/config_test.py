from config import config
import config.helper as cfg_helper


print(config.FACILITY_NAME)
print(config.LOG_FOLDER)
print(config.log_file_name)
print(config.LOG_FILE_PATH)

# exclude duplication
result = cfg_helper.resolve_filename_conflict(
    config.LOG_FILE_PATH, "./test/fixtures/duplication_exist/"
)
print(f"exist duplication: {result}")
result = cfg_helper.resolve_filename_conflict(
    config.LOG_FILE_PATH, "./test/fixtures/duplication_not_exist/"
)
print(f"not exist duplication: {result}")
