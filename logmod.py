import logging
from datetime import datetime as dt
import pathlib
import os
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


def create_logger_file_path(prefix: str):
    log_folder = ROOT_APP_FOLDER / 'logs' / prefix
    log_file_name = f"{prefix}_logger_{dt.now().strftime('%Y_%m_%d')}.log"
    log_path = log_folder / log_file_name
    log_path.parent.mkdir(parents=True, exist_ok=True)
    return log_path


def compose_logger_name(prefix):
    return f'{prefix}_logger'


def logger_factory(prefix):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(' - '.join(FORMAT_LOG_CONSOLE)))

    logfile_path = create_logger_file_path(prefix)
    logfile = logging.FileHandler(logfile_path)
    logfile.setLevel(logging.DEBUG)
    logfile.setFormatter(logging.Formatter(', '.join(FORMAT_LOG_FILE)))

    logger_name = compose_logger_name(prefix)
    _logging = logging.Logger(logger_name)
    _logging.setLevel(logging.DEBUG)
    _logging.addHandler(console)
    _logging.addHandler(logfile)
    return _logging


app_logger = logger_factory('app_logger')
