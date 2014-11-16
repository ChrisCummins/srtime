from datetime import datetime
import logging as log
import os

class Process:
    def _get_tmpfile(self):
        epoch = datetime.utcfromtimestamp(0)
        delta = datetime.now() - epoch
        timestamp = round(delta.total_seconds() * 1000)
        return "/tmp/srtime-{0}".format(timestamp)

    def __init__(self, options):
        cmd = options.command
        tmpfile = self._get_tmpfile()
        cmd += " 2>&1 | tee {0}".format(tmpfile)

        log.info("Command: {0}".format(cmd))

        # Flush the system caches prior to executing the command:
        if options.flush_caches:
            flush_system_caches()

        # Execute the command:
        start = datetime.now()
        os.system(cmd)
        end = datetime.now()

        # Remove tempfile:
        os.system("rm -f {0}".format(tmpfile))

        # Return elapsed time:
        self._time = end - start

    def time(self):
        return self._time.microseconds / 1000
