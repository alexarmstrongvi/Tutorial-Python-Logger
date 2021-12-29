import logger
log = logger.get_logger(__name__)

import argparse
import sys
import os
import subprocess

import module as mod
import subpackage.submodule as submod


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level') # log_level
    args = parser.parse_args()
    return args

def main():
    log.info('='*40)
    for line in logger.log_summary_str(log).split('\n'):
        log.info(line)
    log.info('Info message')
    log.warning('Warning message')
    print('sys.stdout message')
    print('sys.stderr message', file=sys.stderr)

    # Currently not sure if system messages (i.e. fd 1 & 2) can be captured
    subprocess.run('echo Unix stdout message'.split())
    #subprocess.run('echo "Unix stderr message" >&2'.split()) # Doesn't work
    os.system('echo "Unix stderr message" >&2')

    log.info('\r'+' '*80)
    log.info('='*40)

    for line in logger.log_summary_str(mod.log).split('\n'):
        log.info(line)
    mod.print_messages()
    log.info('\r'+' '*80)
    log.info('='*40)

    for line in logger.log_summary_str(submod.log).split('\n'):
        log.info(line)
    submod.print_messages()
    log.info('\r'+' '*80)
    log.info('='*40)

    raise RuntimeError('Test unhandled exception')
    log.info('='*40)

if __name__ == '__main__':
    args = get_args()
    if args.log_level:
        log.setLevel(args.log_level.upper())
    main()
