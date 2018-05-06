from srtime.exceptions import *
from srtime.stats import *
from unittest import TestCase, main


class TestStats(TestCase):

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

  # Stats() tests
  def _test_stats(self, l, confidence, threshold):
    s = Stats(l, confidence=confidence, threshold=threshold)
    cf = confinterval(l, c=confidence, n=threshold)
    self.assertTrue(s.mean == mean(l))
    self.assertTrue(s.c1 == cf[0])
    self.assertTrue(s.c2 == cf[1])
    self.assertTrue(s.confidence == confidence)
    self.assertTrue(s.threshold == threshold)
    self.assertTrue(s.min == min(l))
    self.assertTrue(s.max == max(l))
    self.assertTrue(s.range == range(l))
    self.assertTrue(s.variance == variance(l))
    self.assertTrue(s.n == len(l))

  def _test_stats_empty_list(self):
    return Stats([])

  def test_stats_empty_list(self):
    self.assertRaises(ValueError, self._test_stats_empty_list)

  def test_stats_single_item_list(self):
    self._test_stats([1], 0.5, 10)

  def test_stats_123_list(self):
    self._test_stats([1, 2, 3], 0.5, 10)

  def test_stats_cf(self):
    self._test_stats([1, 2, 3], 0.8, 10)

  def test_stats_threshold(self):
    self._test_stats([1, 2, 3], 0.5, 1)

  # Stats.format() tests
  def test_stats_format(self):
    output = ("95% confidence values from 3 iterations:\n"
              "-0.48 2.0 4.48\n")
    s = Stats([1, 2, 3])
    self.assertTrue(s.format() == output)

  def _test_stats_format_fmt_foobar(self):
    s = Stats([1, 2, 3])
    return s.format(fmt="foobar")

  def _test_stats_format_fmt_10(self):
    s = Stats([1, 2, 3])
    return s.format(fmt=10)

  def test_stats_format_fmt(self):
    s = Stats([1, 2, 3])
    self.assertTrue(isinstance(s.format(fmt="min"), str))
    self.assertTrue(isinstance(s.format(fmt="txt"), str))
    self.assertTrue(isinstance(s.format(fmt="tsv"), str))
    self.assertTrue(isinstance(s.format(fmt="csv"), str))
    self.assertRaises(InvalidParameterException,
                      self._test_stats_format_fmt_foobar)
    self.assertRaises(InvalidParameterException,
                      self._test_stats_format_fmt_10)


if __name__ == '__main__':
  main()
