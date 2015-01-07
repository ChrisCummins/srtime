# A benchmarking timer
[![Build Status](https://travis-ci.org/ChrisCummins/srtime.svg?branch=master)](https://travis-ci.org/ChrisCummins/srtime)
[![Coverage Status](https://img.shields.io/coveralls/ChrisCummins/srtime.svg)](https://coveralls.io/r/ChrisCummins/srtime?branch=master)

The number of "moving parts" in a modern software stack means that
program execution time is non-deterministic. As a result, performance
evaluation should take a statistically rigorous approach, using the
results of multiple iterations to reduce the impact of outliers.

This is a utility for adding statistical rigour to your program
performance evaluations. It repeatedly executes a program for a set
amount of time, then reports mean, lower and upper confidence values.

Here's how you get started:

```
$ srtime ./my_benchmark
95% confidence values from 37 iterations:
103.665 103.699 103.733
```

## Features

* Microsecond precision timing of programs.
* User defined amount of time to collect results for (e.g. 60
  seconds), or a minimum number of iterations to perform (e.g. 100).
* Results can be displayed graphically using the `-g` flag.
* User defined confidence intervals, output precision, and output
  format.
* Can act as a filter for timing critical sections of a program based
  on its output.
* Supports flushing the host system caches before every invocation of
  the target program.

For a list of all of the program features, see `srtime --help`.

## Installation

Install [python](https://www.python.org/) >= 2.6, and the
[python-setuptools](https://pypi.python.org/pypi/setuptools)
package. Then, from this directory, run:

```
sudo python setup.py install
```

## Contribute

* Source Code: http://github.com/ChrisCummins/srtime
* Issue Tracker: https://github.com/ChrisCummins/srtime/issues

Patches welcome!

## Support

If you are having issues, please get in touch: chrisc.101@gmail.com.
