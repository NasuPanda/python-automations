from win32gui import GetForegroundWindow, GetWindowText


class ActiveWindowMonitor:
    """Monitor an active window."""

    def __init__(self, monitoring_apps):
        self.monitoring_apps = monitoring_apps

    @classmethod
    def __remove_unsupported_characters(cls, string, encoding="cp932"):
        # From string, remove characters which is not supported by specified encoding.
        return string.encode(encoding, errors="ignore").decode(encoding)

    @classmethod
    def get_active_window_title(cls):
        """Get the active window title."""
        return cls.__remove_unsupported_characters(GetWindowText(GetForegroundWindow()))

    def exists_active_process(self):
        active_window_title = self.get_active_window_title()
        return any([app_name in active_window_title for app_name in self.monitoring_apps])
