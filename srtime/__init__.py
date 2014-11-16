import sys
import argparse
import logging as log
import random
import numpy as np
import scipy as sp
import scipy.stats
import math
import os
from datetime import datetime
import matplotlib.pyplot as plt

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

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

# Flush system caches on a Linux operating system. Note that this
# requires root privileges, which may result in a password prompt for
# users which have not removed the prompts in their sudoers file.
def flush_system_caches():
    log.info("Flushing system caches")
    os.system('sudo sync && echo "echo 3 > /proc/sys/vm/drop_caches" | sudo sh')

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        argparse.ArgumentParser.__init__(self,
                                         description=("A statistically rigorous "
                                                      "program execution timer."))

        # Define command line arguments:
        self.add_argument("args", nargs="+",
                          help="The command to execute")
        self.add_argument("--version", action="version",
                          version=("%(prog)s version {version}"
                                   .format(version=__version__)))
        self.add_argument("-v", "--verbose", action="store_true",
                          dest="verbose", default=False,
                          help="run verbosely")
        self.add_argument("-i", "--input", action="store_true",
                          dest="input", default=False)
        self.add_argument("-f", "--format", action="store",
                          dest="fmt", default="min",
                          help=("set the output format. "
                                "Valid options are: min,txt,csv,tsv "
                                "[default: %default]"))
        self.add_argument("-m", "--min-iterations", action="store", type=int,
                          dest="min_iterations", default=5,
                          help=("set the minimum number of iterations "
                                "to perform [default: %default]"))
        self.add_argument("-t", "--target-time", action="store", type=int,
                          dest="target_time", default=10,
                          help=("set the target duration of all iterations "
                                "in seconds [default: %default]"))
        self.add_argument("-N", "--threshold", action="store", type=int,
                          dest="threshold", default=30,
                          help=("set the threshold number of iterations to "
                                "switch between Gaussian and t-distributions "
                                "for calculating confidence intervals "
                                "[default: %default]"))
        self.add_argument("-p", "--precision", action="store", type=int,
                          dest="precision", default=3,
                          help=("set the number of digits after a decimal point "
                                "to round to when printing numbers "
                                "[default: %default]"))
        self.add_argument("-c", "--confidence", action="store", type=float,
                          dest="confidence", default=0.95,
                          help=("set the confidence value for calculating "
                                "confidence intervals, 0 < c < 1 "
                                "[default: %default]"))
        self.add_argument("-g", "--graph", action="store_true",
                          dest="graph", default=False,
                          help="display a graph of results")
        self.add_argument("-F", "--flush-cache", action="store_true",
                          dest="flush_caches", default=False,
                          help=("flush system caches before every iteration. "
                                "Note this requires root privileges, and only "
                                "supports Unix operating systems"))

class Results:
    def __init__(self, options):
        self._results = []
        self._options = options

    def append(self, time):
        self._results.append(time)

    # Return the raw array of execution times:
    def times(self):
        return self._results

    def n(self):
        return len(self._results)

    def mean(self):
        return sum(self._results) / len(self._results)

    def min(self):
        return min(self._results)

    def max(self):
        return max(self._results)

    def range(self):
        return self.max() - self.min()

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
                ("range", self.range()),
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

class SRTime:
    def __init__(self, options):
        self._command = options.args
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
        # Perform first trial run:
        p = Process(self._command, self._options).time()

        # Counters:
        i, elapsed_time, avg_p = 0, 0, 0

        # The target amount of time to run for (in ms):
        target_time = self._options.target_time * 1000
        # The minimum number of iterations to run:
        min_iterations = self._options.min_iterations

        # Keep running the command while there is time left, or until
        # we have executed the minimum number of iterations:
        while elapsed_time < target_time - avg_p or i < min_iterations:

            # Logging:
            t_exp = round(avg_p / 1000, 2)
            t_rem = round((target_time - elapsed_time) / 1000, 1)
            log.info("Time remaining: {0}s. Average execution time: {1}s. "
                     "Starting iteration. n = {2}."
                     .format(t_rem, t_exp, i + 1))

            # Run the command:
            p = Process(self._command, self._options).time()
            self._results.append(p)

            # Update the counters:
            elapsed_time += p
            i += 1
            avg_p = self._results.mean()

    def results(self):
        return self._results

# Plot and show a graph of the results for the given command.
def graph(results, command):
    title = ""
    for c in command:
        title += c + " "

    plt.plot(range(1, results.n() + 1), results.times())
    plt.suptitle(title, fontsize=16)
    plt.xlabel('Iteration')
    plt.ylabel('Execution time (ms)')
    plt.xlim(1, results.n())
    plt.show()

def main(argc, argv):
    # Get arguments from command line:
    parser = ArgumentParser()
    args = parser.parse_args()

    # Set program verbosity:
    if args.verbose:
        log.basicConfig(format="%(message)s", level=log.DEBUG)
    else:
        log.basicConfig()

    try:
        # Run timer:
        results = SRTime(args).results()

        # Print results:
        print(results.fmt(args.fmt))

        # Graph results:
        if args.graph:
            graph(results, args)
    except InvalidParameterException as err:
        print(err)
        return 1

    return 0
