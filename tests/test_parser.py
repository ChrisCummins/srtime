from srtime.exceptions import *
from srtime.parser import *
from unittest import TestCase, main


class TestProcess(TestCase):

  def test_parser_args(self):
    l = ["a", "b", "c"]  # Test arguments
    p = ArgumentParser()
    args = p.parse_args(l)
    self.assertTrue(args.args == l)

  def _test_parser_args_none(self):
    l = []  # Test arguments
    p = ArgumentParser()
    args = p.parse_args(l)

  def test_parser_args_none(self):
    self.assertRaises(ArgumentParserException, self._test_parser_args_none)

  def test_parser_command(self):
    l = ["a", "b", "c"]  # Test arguments
    p = ArgumentParser()
    args = p.parse_args(l)
    self.assertTrue(args.command == " ".join(l))

  # Flag: -v / --verbose
  def test_parser_verbose_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertFalse(args.verbose)

  def test_parser_verbose(self):
    args = ArgumentParser().parse_args(["a", "-v"])
    self.assertTrue(args.verbose)
    args = ArgumentParser().parse_args(["a", "--verbose"])
    self.assertTrue(args.verbose)

  # Flag: -i / --filter
  def test_parser_filter_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertFalse(args.filter)

  def test_parser_filter(self):
    args = ArgumentParser().parse_args(["a", "-i"])
    self.assertTrue(args.filter)
    args = ArgumentParser().parse_args(["a", "--filter"])
    self.assertTrue(args.filter)

  # Flag: -f / --format
  def test_parser_format_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertTrue(args.fmt == "min")

  def test_parser_format(self):
    args = ArgumentParser().parse_args(["a", "-f", "txt"])
    self.assertTrue(args.fmt == "txt")
    args = ArgumentParser().parse_args(["a", "--format", "txt"])
    self.assertTrue(args.fmt == "txt")

  # Flag: -m / --min-iterations
  def test_parser_min_iterations_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertTrue(args.min_iterations == 5)

  def test_parser_min_iterations(self):
    args = ArgumentParser().parse_args(["a", "-m", "10"])
    self.assertTrue(args.min_iterations == 10)
    args = ArgumentParser().parse_args(["a", "--min-iterations", "20"])
    self.assertTrue(args.min_iterations == 20)

  # Flag: -t / --target-time
  def test_parser_target_time_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertTrue(args.target_time == 10)

  def test_parser_target_time(self):
    args = ArgumentParser().parse_args(["a", "-t", "30"])
    self.assertTrue(args.target_time == 30)
    args = ArgumentParser().parse_args(["a", "--target-time", "20"])
    self.assertTrue(args.target_time == 20)

  # Flag: -N / --threshold
  def test_parser_threshold_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertTrue(args.threshold == 30)

  def test_parser_threshold(self):
    args = ArgumentParser().parse_args(["a", "-N", "30"])
    self.assertTrue(args.threshold == 30)
    args = ArgumentParser().parse_args(["a", "--threshold", "20"])
    self.assertTrue(args.threshold == 20)

  # Flag: -p / --precision
  def test_parser_precision_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertTrue(args.precision == 3)

  def test_parser_precision(self):
    args = ArgumentParser().parse_args(["a", "-p", "1"])
    self.assertTrue(args.precision == 1)
    args = ArgumentParser().parse_args(["a", "--precision", "2"])
    self.assertTrue(args.precision == 2)

  # Flag: -c / --confidence
  def test_parser_confidence_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertTrue(args.confidence == .95)

  def test_parser_confidence(self):
    args = ArgumentParser().parse_args(["a", "-c", "0.25"])
    self.assertTrue(args.confidence == 0.25)
    args = ArgumentParser().parse_args(["a", "--confidence", "0.5"])
    self.assertTrue(args.confidence == 0.5)

  # Flag: -g / --graph
  def test_parser_graph_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertFalse(args.graph)

  def test_parser_graph(self):
    args = ArgumentParser().parse_args(["a", "-g"])
    self.assertTrue(args.graph)
    args = ArgumentParser().parse_args(["a", "--graph"])
    self.assertTrue(args.graph)

  # Flag: -F / --flush-cache
  def test_parser_flush_caches_default(self):
    args = ArgumentParser().parse_args(["a"])
    self.assertFalse(args.flush_caches)

  def test_parser_flush_caches(self):
    args = ArgumentParser().parse_args(["a", "-F"])
    self.assertTrue(args.flush_caches)
    args = ArgumentParser().parse_args(["a", "--flush-cache"])
    self.assertTrue(args.flush_caches)


if __name__ == '__main__':
  main()
