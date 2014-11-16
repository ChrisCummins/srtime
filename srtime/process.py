from datetime import datetime
import logging as log
import pexpect

from srtime.exceptions import ProcessException

class Process:
    def __init__(self, options):
        # Flush the system caches prior to executing the command:
        if options.flush_caches:
            flush_system_caches()

        # Spawn the process:
        start = datetime.now()
        process = pexpect.spawn(options.args, timeout=None)

        # Buffer the output:
        for line in process:
            print(line.decode('raw_unicode_escape').rstrip())

        # Wait until the process terminates:
        process.close()
        end = datetime.now()

        # Throw an exception if the process exited with non-zero
        # status:
        if process.exitstatus:
            raise ProcessException(options.command, process.exitstatus)

        # Return elapsed time:
        elapsed = end - start
        self._times = [elapsed.microseconds / 1000]

    def times(self):
        return self._times
