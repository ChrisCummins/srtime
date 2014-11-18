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


class Stats:
    def __init__(self, l, confidence=0.95, threshold=30):
        cfint = confinterval(l, confidence, threshold)

        # Ordered attribute pairs:
        self._attrs = [("mean", mean(l)),
                       ("c1", cfint[0]),
                       ("c2", cfint[1]),
                       ("confidence", confidence),
                       ("threshold", threshold),
                       ("min", min(l)),
                       ("max", max(l)),
                       ("range", range(l)),
                       ("variance", variance(l)),
                       ("n", len(l))]

        # Create class attributes from ordered attribute pairs:
        for pair in self._attrs:
            setattr(self, pair[0], pair[1])

    # Return a formatted string:
    def format(self, fmt="min", precision=2):
        def rnd(n, precision=precision):
            return round(n, precision)

        def _raise_param_ex(fmt):
            raise InvalidParameterException("format", fmt,
                                            msg=("Valid formats are: "
                                                 "min, txt, tsv, csv"))

        if not isinstance(fmt, str):
            _raise_param_ex(fmt)

        s = ""

        if fmt.lower() == "min":
            s = ("{c}% confidence values from {n} iterations:\n"
                 .format(c=int(self.confidence * 100),
                         n=self.n))
            s += ("{c1} {mean} {c2}\n"
                  .format(c1=rnd(self.c1),
                          mean=rnd(self.mean),
                          c2=rnd(self.c2)))
        else:
            for stat in self._attrs:
                prop = stat[0]
                val = rnd(stat[1])

                if fmt.lower() == "txt":
                    s += "{0}: {1}\n".format(prop, val)
                elif fmt.lower() == "tsv":
                    s += "{0}\t{1}\n".format(prop, val)
                elif fmt.lower() == "csv":
                    s += '"{0}",{1}\n'.format(prop, val)
                else:
                    _raise_param_ex(fmt)
        return s
