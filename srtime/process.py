import logging as log
import os
from time import time

import pexpect
from srtime.exceptions import FilterInputException, ProcessException


# Flush system caches on a Linux operating system. Note that this
# requires root privileges, which may result in a password prompt for
# users which have not removed the prompts in their sudoers file.
def flush_system_caches():
  log.info("Flushing system caches")
  os.system('sudo sync && '
            'echo "echo 3 > /proc/sys/vm/drop_caches" | sudo sh')


class Process:
  def __init__(self, options):
    self._options = options
    # Create a list to store times in:
    self._times = []

  def run(self):
    options = self._options

    # Flush the system caches prior to executing the command:
    if options.flush_caches:
      flush_system_caches()

    # Pre-execution hook:
    self.pre_exec_hook()

    # Spawn the process:
    process = pexpect.spawn(options.command, timeout=None)

    # Buffer the output line by line:
    for buf in process:
      # Decode the buffered output into a string.
      line = buf.decode('raw_unicode_escape').rstrip()
      # Print the line to stdout if not "quiet".
      if not options.quiet:
        print(line)
      # Process line.
      self.output_hook(line)

    # Wait until the process terminates:
    process.close()
    # Post-execution hook:
    self.post_exec_hook()

    # Throw an exception if the process exited with non-zero
    # status:
    if process.exitstatus:
      raise ProcessException(options.command, process.exitstatus)

  def times(self):
    return self._times

  # Pre-execution hook, called immediately before the process is
  # spawned.
  def pre_exec_hook(self):
    pass

  # Post-execution hook, called immediately after the process
  # terminates.
  def post_exec_hook(self):
    pass

  # Output hook, called for-each line of output buffered from the
  # process.
  def output_hook(self, line):
    pass


# A timed process uses a timer to derive the amount of time taken to
# execute the process.
class TimedProcess(Process):
  # Record the starting time.
  def pre_exec_hook(self):
    self._start = time()

  # Calculate the elapsed time and record it.
  def post_exec_hook(self):
    end = time()
    elapsed = end - self._start
    self._times.append(elapsed)


# A filter process is one which derives its execution times from the
# output of the process.
class FilterProcess(Process):
  # Record the output as a result.
  def output_hook(self, line):
    try:
      self._times.append(float(line))
    except ValueError:
      raise FilterInputException(line)
