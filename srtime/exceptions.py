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


# Exception thrown if the output of a process cannot be filtered.
class FilterInputException(Exception):
  def __init__(self, errline):
    self._errline = errline

  def __str__(self):
    return ("Unable to process the program output. Caused by:\n\n{errline}"
            .format(errline=self._errline))


# Exception thrown by an error parsing arguments.
class ArgumentParserException(Exception): pass
