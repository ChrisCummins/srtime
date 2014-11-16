# Exception thrown for an invalid command line parameter value.
class InvalidParameterException(Exception):
    def __init__(self, param, val, msg=None):
        self._param = param
        self._val = val
        self._msg = msg

    def __str__(self):
        s = ("Invalid value '{0}' for parameter '{1}'!"
             .format(self._val, self._param))
        if self._msg:
            s += "\n{0}.".format(self._msg)
        return s

# Exception thrown if a process exits with a non-zero status.
class ProcessException(Exception):
    def __init__(self, procname, errcode):
        self._procname = procname
        self._errcode = errcode

    def __str__(self):
        return ("Process '{proc}' exited with non-zero status: {errcode}"
                .format(proc=self._procname, errcode=self._errcode))
