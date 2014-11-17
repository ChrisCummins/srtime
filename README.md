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

## Further Reading
1. A. Georges, D. Buytaert, and L. Eeckhout,
   [“Statistically Rigorous Java Performance Evaluation,”](http://www.ccs.neu.edu/racket/Performance/andy-georges-paper.pdf)
   ACM SIGPLAN Not., vol. 42, no. 10, p. 57, Oct. 2007.
