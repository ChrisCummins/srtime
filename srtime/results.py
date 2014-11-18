import numpy as np
import scipy as sp
import scipy.stats
from math import sqrt

import srtime
from srtime.exceptions import InvalidParameterException


# Return the mean value of a list
def mean(l):
    if len(l):
        return sum(l) / len(l)
    else:
        return 0


# Return the range of a list
def range(l):
    if len(l):
        return max(l) - min(l)
    else:
        return 0


# Return the variance of a list
def variance(l):
    if len(l) > 1:
        differences = []
        for n in l:
            differences.append((n - mean(l)) ** 2)
        return sum(differences) / (len(differences) - 1)
    else:
        return 0


# Return the standard deviation of a list
def stdev(l):
    return sqrt(variance(l))


# Return the confidence interval of a list for a given confidence
def confinterval(l, c=0.95, n=30):
    if len(l) > 1:
        scale = stdev(l) / sqrt(len(l))

        if len(l) >= n:
            # For large values of n, use a normal (Gaussian) distribution:
            c1, c2 = scipy.stats.norm.interval(c, loc=mean(l), scale=scale)
        else:
            # For small values of n, use a t-distribution:
            c1, c2 = scipy.stats.t.interval(c, len(l) - 1, loc=mean(l), scale=scale)

        return c1, c2
    else:
        return 0, 0


class Results(list):
    def __init__(self, options):
        self._options = options

    def results(self):
        cfint = confinterval(self, self._options.confidence,
                             self._options.threshold)
        return [("mean", mean(self)),
                ("c1", cfint[0]),
                ("c2", cfint[1]),
                ("minimum", min(self)),
                ("maximum", max(self)),
                ("range", range(self)),
                ("variance", variance(self)),
                ("n", len(self))]

    def fmt_n(self, n):
        return round(n, self._options.precision)

    def fmt(self, fmt):
        s, results = "", self.results()

        if fmt.lower() == "min":
            cfint = confinterval(self, self._options.confidence,
                                 self._options.threshold)
            s = ("{c}% confidence values from {n} iterations:\n"
                 .format(c=round(self._options.confidence * 100),
                         n=len(self)))
            s += ("{c1} {mean} {c2}"
                  .format(c1=self.fmt_n(cfint[0]),
                          mean=self.fmt_n(mean(self)),
                          c2=self.fmt_n(cfint[1])))
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
