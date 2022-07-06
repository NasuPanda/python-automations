"""This module defines exceptions.
"""


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