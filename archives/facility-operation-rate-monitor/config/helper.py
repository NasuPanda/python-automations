import pathlib

import ruamel.yaml

from libs import timehelper


# YAML instance to load and write yaml
yaml = ruamel.yaml.YAML()


def log_file_name(attached_string: str, extension: str = ".csv") -> str:
    """Returns the log file name.
    - Format is `YYMMDD-YYMMDD_attached_string.extension`
        - `YYMMDD-YYMMDD` is first to last day of this month.

    Parameters
    ----------
    attached_name : str
        Attached name to the end.
    extension : str, optional
        File extension, by default ".csv"

    Returns
    -------
    str
        Log file name.
    """
    first_day = timehelper.format(
        timehelper.first_day_of_this_month(), "short"
    )
    last_day = timehelper.format(
        timehelper.last_day_of_this_month(), "short"
    )
    return f"{first_day}-{last_day}_{attached_string}{extension}"


def log_file_fullpath(log_folder: str, log_filename: str) -> str:
    """Returns the log file absolute path.

    Parameters
    ----------
    log_folder : str
        Log file location.
    log_filename : str
        Log file name.

    Returns
    -------
    str
        Log file absolute path.
    """
    log_folder_absolute_path = str(pathlib.Path(log_folder).resolve())
    return f"{log_folder_absolute_path}/{log_filename}"


def load_yaml(yaml_path: str) -> dict:
    """Load yaml data as a dictionary.

    Parameters
    ----------
    yaml_path : str
        YAML file path.

    Returns
    -------
    dict
        Loaded data.
    """
    with open(yaml_path, mode='r+', encoding="utf-8") as stream:
        return yaml.load(stream)


def update_yaml(yaml_path: str, writing_data: dict):
    """Write a dictionary data to yaml.

    Parameters
    ----------
    yaml_path : str
        YAML file path.
    write_data : dict
        Writing data in dict format.
    """
    with open(yaml_path, 'w') as stream:
        yaml.dump(writing_data, stream=stream)
