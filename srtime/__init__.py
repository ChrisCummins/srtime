import logging as log
import matplotlib.pyplot as plt

from srtime.argparse import ArgumentParser
from srtime.exceptions import InvalidParameterException
from srtime.srtime import SRTime

# Flush system caches on a Linux operating system. Note that this
# requires root privileges, which may result in a password prompt for
# users which have not removed the prompts in their sudoers file.
def flush_system_caches():
    log.info("Flushing system caches")
    os.system('sudo sync && echo "echo 3 > /proc/sys/vm/drop_caches" | sudo sh')

# Plot and show a graph of the results for the given command.
def graph(results, command):
    plt.plot(range(1, results.n() + 1), results.times())
    plt.suptitle(command, fontsize=16)
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
            graph(results, args.command)
    except InvalidParameterException as err:
        print(err)
        return 1

    return 0
