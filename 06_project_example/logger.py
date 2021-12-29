import logging
from traceback import TracebackException
import sys

ROOT_CONFIGURED = False

# Format options
#LOG_FMT_DEFAULT ='%(levelname)8s :: %(message)s'
LOG_FMT_DEFAULT ='%(levelname)8s :: %(module)10s :: %(message)s'
#LOG_FMT_DEFAULT = '%(levelname)8s :: (%(filename)s) %(message)s'
#LOG_FMT_DEFAULT ='%(levelname)8s :: [%(asctime)s] (%(filename)s) %(message)s'
#LOG_FMT_DEFAULT = "%(levelname)8s :: (%(module)s - %(funcName)s()) %(message)s"
#LOG_FMT_DEFAULT = "%(levelname)8s :: (%(module)s:%(funcName)s():L%(lineno)d) %(message)s"

def get_logger(name, lvl=None):
    global ROOT_CONFIGURED
    if ROOT_CONFIGURED:
        log = logging.getLogger(name)
        if lvl:
            log.setLevel(lvl.upper())
    elif name != '__main__':
        logging.error('First call to get logger not coming from main script')
        sys.exit()
    else:
        logging.basicConfig(
                stream = sys.stdout,
                format = LOG_FMT_DEFAULT,
                level  = lvl,
        )
        log = logging.getLogger()
        ROOT_CONFIGURED = True

        capture_python_stdout(log)

    return log

def capture_python_stdout(root_log):
    # Source: https://stackoverflow.com/questions/19425736/how-to-redirect-stdout-and-stderr-to-logger-in-python
    def handle_exception(typ, val, tb):
        # Sources:
        # https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
        # https://stackoverflow.com/questions/8050775/using-pythons-logging-module-to-log-all-exceptions-and-errors
        if issubclass(typ, KeyboardInterrupt):
            # Don't capture keyboard interrupt
            sys.__excepthook__(typ, val, tb)
            return
        nonlocal root_log

        # Option 1 - trace in one log error message
        #root_log.exception("Uncaught exception", exc_info=(typ, val, tb))

        # Option 2 - trace split into one log error message per newline
        root_log.error("Uncaught exception")#, exc_info=(typ, val, tb))
        for lines in TracebackException(typ, val, tb).format():
            for line in lines.splitlines():
                root_log.error(line)

    sys.excepthook = handle_exception

    sys.stdout = LoggerWriter(root_log.info)
    sys.stderr = LoggerWriter(root_log.warning) # root_log.error?


class LoggerWriter(object):
    def __init__(self, writer):
        self._writer = writer
        self._msg = ''

    def write(self, message):
        self._msg = self._msg + message
        while '\n' in self._msg:
            pos = self._msg.find('\n')
            self._writer(self._msg[:pos])
            self._msg = self._msg[pos+1:]

    def flush(self):
        if self._msg != '':
            self._writer(self._msg)
            self._msg = ''


def log_multiline(log_call, txt):
    for line in txt.split('\n'):
        log_call(line)

def log_summary_str(log):

    log_lvl = log.level
    eff_lvl = log.getEffectiveLevel()
    min_lvl = min([lvl for lvl  in range(logging.CRITICAL) if log.isEnabledFor(lvl)])

    s  = f'Log Summary - {log.name}'
    s += f'\n - Levels   : Effective = {eff_lvl}; Logger = {log_lvl}; Enabled for >={min_lvl}'
    s += f'\n - Flags    : Disabled = {log.disabled}'
    s += f', Propogate = {log.propagate}'
    s += f', Handlers = {log.hasHandlers()}'
    #if log.parent:
    #    s += f'\n - Parent : {log.parent.name}'
    for i, hndl in enumerate(log.handlers,1):
        s += f'\n - Handler {i}: {hndl}'
    for i, fltr in enumerate(log.filters,1):
        s += f'\n - Filter {i} : {fltr}'
    return s

def capture_unix_fd():
    return
    # Currently doesn't work
    # Also risk of infinite pipe loop as python stdout gets redirected back
    # to logger that prints it to stdour
    # Source: https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file
    import subprocess, os, sys

    tee = subprocess.Popen(["tee", "log.txt"], stdin=subprocess.PIPE)
    # Cause tee's stdin to get a copy of our stdin/stdout (as well as that
    # of any child processes we spawn)
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())

    # The flush flag is needed to guarantee these lines are written before
    # the two spawned /bin/ls processes emit any output
    print("\nstdout", flush=True)
    print("stderr", file=sys.stderr, flush=True)

    # These child processes' stdin/stdout are
    os.spawnve("P_WAIT", "/bin/ls", ["/bin/ls"], {})
    os.execve("/bin/ls", ["/bin/ls"], os.environ)

