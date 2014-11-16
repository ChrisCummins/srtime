from datetime import datetime
import logging as log
import pexpect

from srtime.exceptions import ProcessException

class Process:
    def __init__(self, options):
        # Create a list to store times in:
        self._times = []

        # Flush the system caches prior to executing the command:
        if options.flush_caches:
            flush_system_caches()

        # Spawn the process:
        start = datetime.now()
        process = pexpect.spawn(options.args, timeout=None)

        # Buffer the output line by line:
        for buf in process:
            # Decode the buffered output into a string.
            line = buf.decode('raw_unicode_escape').rstrip()

            # Print the line to stdout.
            print(line)

        # Wait until the process terminates:
        process.close()
        end = datetime.now()

        # Throw an exception if the process exited with non-zero
        # status:
        if process.exitstatus:
            raise ProcessException(options.command, process.exitstatus)

        # If we're not in filtering mode, then record the elapsed
        # time:
        if not options.filter:
            elapsed = end - start
            self._times.append(elapsed.microseconds / 1000)

    def times(self):
        return self._times
