import logger

log = logger.get_module_logger(__name__)

def do_something():
    log.warning("Warning message")
    log.info("Info message")
    log.debug("Debug message")

