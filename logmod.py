from datetime import datetime as dt
import logging
import os
import pathlib


ROOT_APP_FOLDER = pathlib.Path(os.path.abspath(__file__)).parent


FORMAT_LOG_CONSOLE = [
    '%(asctime)s',
    '%(levelname)s',
    '%(funcName)s',
    '%(message)s'
]


FORMAT_LOG_FILE = [
    '{"dt": ' + '"%(asctime)s"',
    '"fn": ' + '"%(filename)s"',
    '"ln": ' + '"%(levelno)s"',
    '"l": ' + '"%(levelname)s"',
    '"m": ' + '"%(module)s"',
    '"fnc": ' + '"%(funcName)s"',
    '"lno": ' + '"%(lineno)d"',
    '"msg": ' + '%(message)s}'
    # '%(processName)s',
    # '%(process)d',
    # '%(threadName)s',
    # '%(thread)d',
]


def compose_logger_name(prefix):
    return f'{prefix}_logger'


def logger_factory(prefix):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(' - '.join(FORMAT_LOG_CONSOLE)))

    logger_name = compose_logger_name(prefix)
    _logging = logging.Logger(logger_name)
    _logging.setLevel(logging.DEBUG)
    _logging.addHandler(console)
    return _logging


app_logger = logger_factory('app_logger')
