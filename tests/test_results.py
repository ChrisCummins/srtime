from unittest import TestCase

import srtime
from srtime.results import *

class TestResults(TestCase):

    # mean() tests
    def test_mean_empty_list(self):
        l = []
        self.assertTrue(mean(l) == 0)

    def test_mean_single_item_list(self):
        l = [1]
        self.assertTrue(mean(l) == 1)

    def test_mean_123_list(self):
        l = [1, 2, 3]
        self.assertTrue(mean(l) == 2)

    # range() tests
    def test_range_empty_list(self):
        l = []
        self.assertTrue(range(l) == 0)

    def test_range_single_item_list(self):
        l = [1]
        self.assertTrue(range(l) == 0)

    def test_range_123_list(self):
        l = [1, 2, 3]
        self.assertTrue(range(l) == 2)

    # variance() tests
    def test_variance_empty_list(self):
        l = []
        self.assertTrue(variance(l) == 0)

    def test_variance_single_item_list(self):
        l = [1]
        self.assertTrue(variance(l) == 0)

    def test_variance_123_list(self):
        l = [1, 2, 3]
        self.assertTrue(variance(l) == 1)

    # stdev() tests
    def test_stdev_empty_list(self):
        l = []
        self.assertTrue(stdev(l) == 0)

    def test_stdev_single_item_list(self):
        l = [1]
        self.assertTrue(stdev(l) == 0)

    def test_stdev_123_list(self):
        l = [1, 2, 3]
        self.assertTrue(stdev(l) == 1)

    # confinterval() tests
    def test_confinterval_empty_list(self):
        l = []
        self.assertTrue(confinterval(l) == (0, 0))

    def test_confinterval_single_item_list(self):
        l = [1]
        self.assertTrue(confinterval(l) == (0, 0))

    def test_confinterval_123_list(self):
        l = [1, 2, 3]
        self.assertTrue(confinterval(l) ==
                        (-0.48413771184375287, 4.4841377118437524))

    def test_confinterval_c50(self):
        l = [1, 2, 3]
        self.assertTrue(confinterval(l, c=0.5) ==
                        (1.528595479208968, 2.4714045207910322))

    def test_confinterval_t_dist(self):
        l = [1, 2, 3]
        self.assertTrue(confinterval(l, n=1) ==
                        (0.86841426592382809, 3.1315857340761717))
