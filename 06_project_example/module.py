import logger
import sys
log = logger.get_logger(__name__)

def print_messages():
    log.info('Module info message')
    log.warning('Module warning message')
    print('Module sys.stdout message')
    print('Module sys.stderr message', file=sys.stderr)
