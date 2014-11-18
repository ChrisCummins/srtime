import math
import numpy as np
import scipy as sp
import scipy.stats

import srtime
from srtime.exceptions import InvalidParameterException


class Results(list):
    def __init__(self, options):
        self._options = options

    def mean(self):
        return sum(self) / len(self)

    def range(self):
        return max(self) - min(self)

    def variance(self):
        differences = []
        mean = self.mean()
        for n in self:
            differences.append((n - mean) ** 2)
        return sum(differences) / (len(differences) - 1)

    def std(self):
        return math.sqrt(self.variance())

    def sem(self):
        return scipy.stats.sem(np.array(self))

    def confidence(self):
        confidence = self._options.confidence
        threshold = self._options.threshold
        scale = self.std() / math.sqrt(len(self))

        if len(self) >= 30:
            # For large values of n, use a normal (Gaussian) distribution:
            c1, c2 = scipy.stats.norm.interval(confidence, loc=self.mean(),
                                               scale=scale)
        else:
            # For small values of n, use a t-distribution:
            c1, c2 = scipy.stats.t.interval(confidence, len(self) - 1,
                                            loc=self.mean(), scale=scale)
        return c1, c2

    def results(self):
        self.confidence()
        return [("mean", self.mean()),
                ("c1", self.confidence()[0]),
                ("c2", self.confidence()[1]),
                ("minimum", min(self)),
                ("maximum", max(self)),
                ("range", self.range()),
                ("variance", self.variance()),
                ("n", len(self))]

    def fmt_n(self, n):
        return round(n, self._options.precision)

    def fmt(self, fmt):
        s, results = "", self.results()

        if fmt.lower() == "min":
            confidence = self.confidence()
            s = ("{c}% confidence values from {n} iterations:\n"
                 .format(c=round(self._options.confidence * 100),
                         n=len(self)))
            s += ("{c1} {mean} {c2}"
                  .format(c1=self.fmt_n(confidence[0]),
                          mean=self.fmt_n(self.mean()),
                          c2=self.fmt_n(confidence[1])))
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
