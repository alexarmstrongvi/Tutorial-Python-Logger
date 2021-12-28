import logger
log = logger.get_logger(__name__)

def print_messages():
    log.info('Module info message')
    log.warning('Module warning message')
