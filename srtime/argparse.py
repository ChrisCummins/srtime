import argparse

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        argparse.ArgumentParser.__init__(
            self,
            description=("A statistically rigorous program execution timer."),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # Define command line arguments:
        self.add_argument("args", nargs="+",
                          help="the command to execute")
        self.add_argument("--version", action="version",
                          version=("%(prog)s version {version}"
                                   .format(version=__version__)))
        self.add_argument("-v", "--verbose", action="store_true",
                          dest="verbose", default=False,
                          help="run verbosely")
        self.add_argument("-i", "--filter", action="store_true",
                          dest="filter", default=False,
                          help="filter execution times from process output")
        self.add_argument("-f", "--format", action="store",
                          dest="fmt", default="min", metavar="<f>",
                          help=("set the output format. "
                                "Valid options are: min,txt,csv,tsv"))
        self.add_argument("-m", "--min-iterations", action="store", type=int,
                          dest="min_iterations", default=5, metavar="<n>",
                          help=("set the minimum number of iterations "
                                "to perform"))
        self.add_argument("-t", "--target-time", action="store", type=int,
                          dest="target_time", default=10, metavar="<t>",
                          help=("set the target duration of all iterations "
                                "in seconds"))
        self.add_argument("-N", "--threshold", action="store", type=int,
                          dest="threshold", default=30, metavar="<n>",
                          help=("set the threshold number of iterations to "
                                "switch between Gaussian and t-distributions "
                                "for calculating confidence intervals"))
        self.add_argument("-p", "--precision", action="store", type=int,
                          dest="precision", default=3, metavar="<n>",
                          help=("set the number of digits after a decimal point "
                                "to round to when printing numbers"))
        self.add_argument("-c", "--confidence", action="store", type=float,
                          dest="confidence", default=0.95, metavar="<c>",
                          help=("set the confidence value for calculating "
                                "confidence intervals, 0 < c < 1"))
        self.add_argument("-g", "--graph", action="store_true",
                          dest="graph", default=False,
                          help="display a graph of results")
        self.add_argument("-F", "--flush-cache", action="store_true",
                          dest="flush_caches", default=False,
                          help=("flush system caches before every iteration. "
                                "Note this requires root privileges, and only "
                                "supports Unix operating systems"))

    # We override the base parse_args() method so that we can inject
    # additional data into the returning arguments namespace.
    def parse_args(self):
        args = super(ArgumentParser, self).parse_args()

        # Add a string "command" which has a concatenated version of
        # the args:
        command = ""
        for arg in args.args:
            command += arg + " "
        args.command = command[:-1]

        return args
