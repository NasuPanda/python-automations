import config.helper as cfg_helper


# exclude duplication
result = cfg_helper.resolve_filename_conflict(
    "220701-220731_A", "./test/fixtures/duplication_exist/"
)
print(f"exist duplication: {result}")
result = cfg_helper.resolve_filename_conflict(
    "220701-220731_A", "./test/fixtures/duplication_not_exist/"
)
print(f"not exist duplication: {result}")
