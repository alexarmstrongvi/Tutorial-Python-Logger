#!/usr/bin/env python3

################################################################################
# Code
################################################################################
# Import project's custom logger module and create top level logger
import logger

## Configuration
log_lvl = 'warning'

# Format options
# stdout/stderr logs should give you just enough info to show what the code is doing and if something went wrong
#log_fmt ='%(levelname)8s :: %(message)s' 
log_fmt ='%(levelname)8s :: (%(filename)s) %(message)s' 
#log_fmt ='%(levelname)8s :: [%(asctime)s] (%(filename)s) %(message)s' 

# log files should have all the info needed to track down bugs and compare outputs between runs
# I prefer log files to be identical run to run if nothing changes (e.g. no timestamps or randomness).
# That way diff'ing log files helps highlight when something subtle changes
file_fmt = ("%(levelname)8s :: (%(module)s - %(funcName)s()) %(message)s")
#file_fmt = ("%(levelname)8s :: (%(module)s:%(funcName)s():L%(lineno)d) %(message)s")

# Get Logger (must be done before importing other modules)
log = logger.get_top_level_logger( __name__, log_lvl, log_fmt,
        # Optional
        output_file='my_output.log',
        file_lvl = 'info',
        file_fmt = file_fmt,
        )

# Import modules that may have their own logger
import log_msg_module

def main():
    log.info('Running Main')
    
    log.info("Info message")
    log.debug("Debug message")
    
    log_msg_module.do_something()
    
    log.info("Done")

if __name__ == "__main__":
    main()
