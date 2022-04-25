from src.Controllers.controller import Controller


class Handler:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.functions = {
            "-USER_UTIL_PWT-": self.controller.input_user_util_pwt,
            "-SELECT_FOLDER-": self.controller.select_folder,
            "-SELECT_FILES-": self.controller.select_files,
            "-SRC_FOLDER-": self.controller.input_img_folder,
            "-SRC_FILES-": self.controller.input_img_files,
            "-SUBMIT-": self.controller.click_submit,
        }

    def handle(self, key, values):
        if key not in self.functions:
            return
        event = self.functions[key]
        event(values)