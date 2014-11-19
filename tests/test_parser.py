from unittest import TestCase, main

import srtime
from srtime.exceptions import *
from srtime.parser import *

class TestProcess(TestCase):

    def test_parser_args(self):
        l = ["a", "b", "c"] # Test arguments
        p = ArgumentParser()
        args = p.parse_args(l)
        self.assertTrue(args.args == l)

    def _test_parser_args_none(self):
        l = [] # Test arguments
        p = ArgumentParser()
        args = p.parse_args(l)

    def test_parser_args_none(self):
        self.assertRaises(ArgumentParserException, self._test_parser_args_none)

    def test_parser_command(self):
        l = ["a", "b", "c"] # Test arguments
        p = ArgumentParser()
        args = p.parse_args(l)
        self.assertTrue(args.command == " ".join(l))


if __name__ == '__main__':
    main()
