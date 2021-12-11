import logging
import sys

TOP_LEVEL_LOGGER_NAME = None

def get_top_level_logger(name, 
                         lvl,
                         fmt,
                         output_file=None,
                         file_lvl=None,
                         file_fmt=None):

    global TOP_LEVEL_LOGGER_NAME
    if TOP_LEVEL_LOGGER_NAME:
        return logging.getLogger(TOP_LEVEL_LOGGER_NAME)
    
    TOP_LEVEL_LOGGER_NAME = name
    lvl = lvl.upper()
    
    # Create logger
    log = logging.getLogger(name)
    log.setLevel(1)

    # StreamHandler
    formatter = logging.Formatter(fmt)
    handler = logging.StreamHandler() # default stream = sys.stderr
    handler.setLevel(lvl)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # FileHandler
    if output_file:
        if file_lvl:
            lvl = file_lvl.upper()
        if file_fmt:
            formatter = logging.Formatter(file_fmt)
        handler = logging.FileHandler(output_file, mode='w')
        handler.setLevel(lvl)
        handler.setFormatter(formatter)
        log.addHandler(handler)

    return log

# TODO: module specific log level and formatting
def get_module_logger(module_name):
    global TOP_LEVEL_LOGGER_NAME
    if TOP_LEVEL_LOGGER_NAME is None:
        print("ERROR :: Cannot get module logger. Top level logger not created.")
        return
    
    return logging.getLogger(TOP_LEVEL_LOGGER_NAME).getChild(module_name)
