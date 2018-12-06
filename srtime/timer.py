import logging as log
from time import time

from srtime.exceptions import InvalidParameterException
from srtime.process import FilterProcess, TimedProcess
from srtime.stats import mean


class Timer:
  def __init__(self, options):
    self._options = options
    self._results = []

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
    # Counters:
    i, elapsed_time, avg_p = 0, 0, 0

    # The target amount of time to run for (in ms):
    target_time = self._options.target_time
    # The minimum number of iterations to run:
    min_iterations = self._options.min_iterations

    # Keep running the command while there is time left, or until
    # we have executed the minimum number of iterations:
    while elapsed_time < target_time - avg_p or i < min_iterations:
      start_time = time()

      # Logging:
      t_exp = round(avg_p / 1000, 2)
      t_rem = max(round(target_time - elapsed_time, 1), 0)
      log.info("Time remaining: {0}s. Average execution time: {1}s. "
               "Starting iteration. n = {2}."
               .format(t_rem, t_exp, i + 1))

      # Create a process:
      if self._options.filter:
        process = FilterProcess(self._options)
      else:
        process = TimedProcess(self._options)

      # Execute the process:
      process.run()
      # Gather results:
      times = process.times()
      self._results += times

      # Update the counters:
      i += len(times)
      avg_p = mean(self._results)
      elapsed_time += time() - start_time

  def results(self):
    return self._results
