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
