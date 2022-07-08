"""This module defines exceptions.
"""


class ReadOnlyError(ValueError):
    """When attempting to change the value of a read-only property.
    """
    pass


class TimeHelperError(Exception):
    """Base exception of time helper.
    """
    pass


class InvalidFormatError(TimeHelperError):
    """When time helper receives an invalid format.
    """
    pass


class ConfigError(Exception):
    """Base exception of config.
    """
    pass


class NumberNotFoundError(ConfigError):
    """When number is not found.
    """
    pass


class ArrayLengthNotMatchError(ConfigError):
    """When array length not matched.
    """
    pass


class MonitorError(Exception):
    """Base exception of monitor module.
    """
    pass


class ProcessTooManyError(MonitorError):
    """When process is too many.
    """
    pass


class InitializerError(MonitorError):
    """When failure to initialize an instance.
    """
    pass
