# Tutorial-Python-Logger
Collection of examples/guides/explanations for using python logger module

See the [wiki](https://github.com/alexarmstrongvi/Tutorial-Python-Logger/wiki) for more info

* Goals for using logger across project
    * [X] Single function call in any module to create logger object
    * [X] Logger object globally accessible in any module
    * [X] Default configuration defined in one place
    * [X] Level configurable with user arguments to main executable
    * [X] Manually configure logger level in a specific module if desired
    * [] Separate handlers easily setup if desired
    * [X] Modules that might be main executable or imported module
    * [X] Captures messages to stdout/stderr (e.g. exceptions, module warnings)
        * https://stackoverflow.com/questions/19425736/how-to-redirect-stdout-and-stderr-to-logger-in-python
        * https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file
    * [] Correlate log indentation with stack depth
