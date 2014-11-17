# A benchmarking timer
[![Build Status](https://travis-ci.org/ChrisCummins/srtime.svg?branch=master)](https://travis-ci.org/ChrisCummins/srtime)
[![Coverage Status](https://img.shields.io/coveralls/ChrisCummins/srtime.svg)](https://coveralls.io/r/ChrisCummins/srtime?branch=master)

Evaluating the performance of benchmarks and programs is
difficult. There are many "moving parts" in the modern software stack,
from frequency governors to system load, garbage collectors, and CPU
schedulers.

This is a timer for performing statistically rigorous performance
evaluation. It executes a given program multiple times and reports the
mean result, and lower and upper confidence values.

## Features

* Microsecond precision timing of programs.
* If you only want to time a critical section from within your
  program, this tool can record the execution times from the output of
  the program itself.
* Supports user-configurable confidence intervals, and output
  precision and format.
* Set the amount of time to collect results for (e.g. 60 seconds), or
  the minimum number of iterations to perform (e.g. 100).
* Supports flushing the host system caches before every invocation of
  the target program.
* Results can be displayed graphically using the `-g` flag.

## Example usage

```
$ srtime ./my_benchmark
95% confidence values from 96 iterations:
103.665 103.699 103.733
```

## Installation

```
sudo python setup.py install
```

## Requirements

* python >= 2.6
* python-setuptools

## Further Reading
1. A. Georges, D. Buytaert, and L. Eeckhout,
   [“Statistically Rigorous Java Performance Evaluation,”](http://www.ccs.neu.edu/racket/Performance/andy-georges-paper.pdf)
   ACM SIGPLAN Not., vol. 42, no. 10, p. 57, Oct. 2007.
