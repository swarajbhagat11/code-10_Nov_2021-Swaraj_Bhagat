import logging

def get_logger():
    logs = logging.getLogger()
    logs.setLevel(level='INFO')
    return logs

logger = get_logger()
