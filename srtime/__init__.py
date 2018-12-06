import logging as log
import sys

import matplotlib.pyplot as plt
from srtime.exceptions import ProcessException
from srtime.parser import ArgumentParser
from srtime.stats import Stats
from srtime.timer import Timer


# Plot and show a graph of the results for the given command.
def graph(results, command):
  plt.plot(range(1, len(results) + 1), results)
  plt.suptitle(command, fontsize=16)
  plt.xlabel('Iteration')
  plt.ylabel('Execution time (ms)')
  plt.xlim(1, len(results))
  plt.show()


def run(options):
  # Run the timer and gather the results:
  return Timer(options).results()


# If no "args" are supplied, they will be taken from the process
# environment.
def main(args=None):
  # Get arguments from command line:
  try:
    parser = ArgumentParser()
    args = parser.parse_args(args)

    # Set program verbosity:
    if args.verbose:
      log.basicConfig(format="%(message)s", level=log.DEBUG)
    else:
      log.basicConfig()

    # Run timer:
    results = run(args)
    stats = Stats(results, confidence=args.confidence,
                  threshold=args.threshold)

    # Print results:
    sys.stderr.write(stats.format(fmt=args.fmt, precision=args.precision))
    sys.stderr.flush()

    # Graph results:
    if args.graph:
      graph(results, args.command)
  except ProcessException as err:
    # If the process fails with a non-zero return code, then print
    # the exception message and return the error code.
    print(err)
    return err._errcode
  except Exception as err:
    print(err)
    return 1

  return 0
