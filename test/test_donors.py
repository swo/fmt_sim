# author: scott olesen <swo@mit.edu>

'''
tests for donors.py
'''

import pytest
from fmt_sim import donors

class TestGenerate:
    def test_correct_length(self):
        lst = list(donors.generate(10, 50, 0.5))
        assert len(lst) == 50
        for line in lst:
            assert len(line.rstrip()) == 10

    def test_correct_donors_bad(self):
        lst = list(donors.generate(10, 50, 0.0))
        for line in lst:
            assert line.rstrip() == "0" * 10

    def test_correct_donors_good(self):
        lst = list(donors.generate(10, 50, 1.0))
        for line in lst:
            assert line.rstrip() == "1" * 10

class TestParse:
    def test_correct(self):
        lst = ["000\n", "010\n", "111\n"]
        assert list(donors.parse(lst)) == [[0, 0, 0], [0, 1, 0], [1, 1, 1]]

    def test_fail_value(self):
        lst = ["foo\n"]
        with pytest.raises(ValueError):
            list(donors.parse(lst))

    def test_fail_run(self):
        lst = ["555\n"]
        with pytest.raises(RuntimeError):
            list(donors.parse(lst))
