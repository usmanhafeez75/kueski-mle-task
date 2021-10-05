# coding: utf8
import logging
from datetime import datetime
from functools import wraps

from ruamel import yaml


def read_yaml(yaml_file: str) -> dict:
    """
    Parse any valid yaml/yml file

    Args:
        yaml_file: yaml file path

    Returns:
        dict
    """
    with open(yaml_file, 'r', encoding="utf8") as _file:
        _dict = yaml.safe_load(_file)
        logging.info(f"Yaml file {yaml_file} parsed!")

    return _dict


def log_time(f):
    @wraps(f)
    def inner(*args, **kwargs):
        start = datetime.now()
        print("{} - {} START".format(start, f.__name__), flush=True)
        response = f(*args, **kwargs)
        print("{} - {} END   duration: {}".format(datetime.now(), f.__name__, datetime.now() - start), flush=True)
        return response

    return inner
