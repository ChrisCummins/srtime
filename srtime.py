#!/usr/bin/env python3

import sys
import optparse
import logging as log
import random
import numpy as np
import scipy as sp
import scipy.stats
import math
import os
from datetime import datetime

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

def version_and_quit(*data):
    print("srtime version 0.0.1")
    print("Copyright (c) 2014 Chris Cummins")
    sys.exit(0)

class OptionParser(optparse.OptionParser):
    def __init__(self):
        optparse.OptionParser.__init__(self)

        # Allow overriding the default handlers:
        self.set_conflict_handler("resolve")

        # Define command line options:
        self.add_option("--version", action="callback",
                        callback=version_and_quit)
        self.add_option("-v", "--verbose", action="store_true",
                        dest="verbose", default=False)
        self.add_option("-i", "--input", action="store_true",
                        dest="input", default=False)
        self.add_option("-f", "--format", action="store", type="string",
                        dest="fmt", default="min")
        self.add_option("-n", "--number", action="store", type="int",
                        dest="number", default=10)
        self.add_option("-N", "--threshold", action="store", type="int",
                        dest="threshold", default=30)
        self.add_option("-p", "--precision", action="store", type="int",
                        dest="precision", default=3)
        self.add_option("-c", "--confidence", action="store", type="float",
                        dest="confidence", default=0.05)

class Results:
    def __init__(self, options):
        self._results = []
        self._options = options

    def append(self, time):
        self._results.append(time)

    def n(self):
        return len(self._results)

    def mean(self):
        return sum(self._results) / len(self._results)

    def min(self):
        return min(self._results)

    def max(self):
        return max(self._results)

    def variance(self):
        differences = []
        mean = self.mean()
        for n in self._results:
            differences.append((n - mean) ** 2)
        return sum(differences) / (len(differences) - 1)

    def std(self):
        return math.sqrt(self.variance())

    def sem(self):
        return scipy.stats.sem(np.array(self._results))

    def confidence(self):
        confidence = self._options.confidence
        threshold = self._options.threshold
        scale = self.std() / math.sqrt(self.n())

        if self.n() >= 30:
            # For large values of n, use a normal (Gaussian) distribution:
            c1, c2 = scipy.stats.norm.interval(confidence, loc=self.mean(),
                                               scale=scale)
        else:
            # For small values of n, use a t-distribution:
            c1, c2 = scipy.stats.t.interval(confidence, self.n() - 1,
                                            loc=self.mean(), scale=scale)
        return c1, c2

    def results(self):
        self.confidence()
        return [("mean", self.mean()),
                ("c1", self.confidence()[0]),
                ("c2", self.confidence()[1]),
                ("minimum", self.min()),
                ("maximum", self.max()),
                ("variance", self.variance()),
                ("n", self.n())]

    def fmt_n(self, n):
        return round(n, self._options.precision)

    def fmt(self, fmt):
        s, results = "", self.results()

        if fmt.lower() == "min":
            confidence = self.confidence()
            s = "{0} {1} {2}".format(self.fmt_n(confidence[0]),
                                     self.fmt_n(self.mean()),
                                     self.fmt_n(confidence[1]))
        else:
            for t in results:
                prop = t[0]
                val = self.fmt_n(t[1])

                if fmt.lower() == "txt":
                    s += "{0}: {1}\n".format(prop, val)
                elif fmt.lower() == "tsv":
                    s += "{0}\t{1}\n".format(prop, val)
                elif fmt.lower() == "csv":
                    s += '"{0}",{1}\n'.format(prop, val)
                else:
                    raise InvalidParameterException("format", fmt,
                                                    msg=("Valid formats are: "
                                                         "min, txt, tsv, csv"))

        return s

class Process:
    def _get_tmpfile(self):
        epoch = datetime.utcfromtimestamp(0)
        delta = datetime.now() - epoch
        timestamp = round(delta.total_seconds() * 1000)
        return "/tmp/srtime-{0}".format(timestamp)

    def _get_cmd(self, command):
        cmd = ""
        for c in command:
            cmd += c + " "
        return cmd

    def __init__(self, command, options):
        cmd = self._get_cmd(command)
        tmpfile = self._get_tmpfile()
        cmd += "2>&1 | tee {0}".format(tmpfile)

        log.info("Command: {0}".format(cmd))

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

class SRTime:
    def __init__(self, command, options):
        self._command = command
        self._options = options
        self._results = Results(options)

        # Check that options are valid:
        if (options.confidence >= 1 or options.confidence <= 0):
            raise InvalidParameterException("confidence",
                                            options.confidence,
                                            msg=("Confidence value must be "
                                                 "within range: 0 <= c <= 1"))

        if (options.threshold <= 0):
            raise InvalidParameterException("threshold",
                                            options.threshold,
                                            msg=("Threshold value must be "
                                                 "greater than 0"))

        log.info("Significance: {0}.".format(round(1 - options.confidence, 2)))
        log.info("Threshold: {0}.".format(options.threshold))

        # Run the command:
        self.run()

    def run(self):
        for i in range(self._options.number):
            log.info("Starting iteration. n = {0}".format(i + 1))
            self._results.append(Process(self._command, self._options).time())

    def results(self):
        return self._results

def main(argc, argv):
    # Get arguments from command line:
    parser = OptionParser()
    (options, args) = parser.parse_args()

    # Set program verbosity:
    if options.verbose:
        log.basicConfig(format="%(message)s", level=log.DEBUG)
    else:
        log.basicConfig()

    try:
        # Run timer:
        t = SRTime(args, options)

        # Print results:
        print(t.results().fmt(options.fmt))
    except InvalidParameterException as err:
        print(err)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
