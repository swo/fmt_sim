# author: scott olesen <swo@mit.edu>

'''
tests for donors.py
'''

import pytest
import io, warnings
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

    def test_no_warn(self):
        # 60 donors should be OK
        lst = ["0" * 60]
        with pytest.warns(None) as record:
            list(donors.parse(lst))

        assert len(record) == 0

    def test_warn(self):
        # but 61 should cause a problem
        lst = ["0" * 61]
        with pytest.warns(UserWarning):
            list(donors.parse(lst))


class TestWrite:
    def test_correct(self):
        f = io.StringIO()
        donors.write(5, 10, 0.5, f)
        f.seek(0)
        lines = [l.rstrip() for l in f.readlines()]
        assert len(lines) == 10

        for line in lines:
            assert len(line) == 5
            assert set(line) <= {'0', '1'}
