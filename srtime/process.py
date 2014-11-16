from datetime import datetime
import logging as log
import pexpect


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


        # Return elapsed time:
        self._time = end - start

    def time(self):
        return self._time.microseconds / 1000
