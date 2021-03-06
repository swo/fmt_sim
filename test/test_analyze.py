# author: scott olesen <swo@mit.edu>

'''
tests for donors.py
'''

import pytest
import numpy as np, io
from fmt_sim import analyze

class TestClopper:
    # I computed these comparison values using R's binom.test

    def test_correct(self):
        lo, hi = analyze.clopper_pearson(100, 200)
        assert (round(lo, 3), round(hi, 3)) == (0.429, 0.571)

    def test_correct2(self):
        lo, hi = analyze.clopper_pearson(20, 400)
        assert (round(lo, 4), round(hi, 4)) == (0.0308, 0.0762)

    def test_correct3(self):
        lo, hi = analyze.clopper_pearson(20, 400, conf=0.90)
        assert (round(lo, 4), round(hi, 4)) == (0.0334, 0.0718)


class TestFisher:
    def test_correct(self):
        value = analyze.fisher_exact_p(10, 1, 11)
        # cf. R: fisher.test(matrix(c(10, 1, 1, 10), nrow=2), alt='greater')
        assert(round(value, 6) == 0.000173)

    def test_memoize(self):
        '''make sure memoization isn't broken'''
        value = analyze.fisher_exact_p(10, 1, 11)
        value = analyze.fisher_exact_p(10, 1, 11)
        value = analyze.fisher_exact_p(10, 1, 11)
        assert(round(value, 6) == 0.000173)


class TestParseHistory:
    def test_correct(self):
        assert analyze.parse_history_line('AsBfCs') == (2, 3)

    def test_correct_with_confusing_donor(self):
        # 's' can be a donor ID, watch out!
        assert analyze.parse_history_line('sfsfsf') == (0, 3)

    def test_wrong_response_indicators(self):
        with pytest.raises(RuntimeError):
            analyze.parse_history_line('AsBsCx')

    def test_wrong_donor_id(self):
        with pytest.raises(RuntimeError):
            analyze.parse_history_line('AsBs@s')


class TestPower:
    def test_correct(self):
        # there are 50 tests that give p < 0.05; another 50 have p > 0.05
        tx_hist = ['As' * 10] * 50 + ['Af' * 10] * 50
        pl_hist = ['PsPf' * 5] * 100

        center = 0.5
        lo, hi = analyze.clopper_pearson(50, 100, conf=0.95)

        assert (lo, center, hi) == analyze.power(tx_hist, pl_hist)

    def test_raise(self):
        with pytest.raises(RuntimeError):
            analyze.power([], [])

class TestWritePower:
    def test_correct(self):
        tx_hist = ['As' * 10] * 50 + ['Af' * 10] * 50
        pl_hist = ['PsPf' * 5] * 100

        center = 0.5
        lo, hi = analyze.clopper_pearson(50, 100, conf=0.95)

        f = io.StringIO()
        analyze.write_power(tx_hist, pl_hist, f)
        f.seek(0)
        lo2, center2, hi2 = [float(x) for x in f.read().rstrip().split("\t")]
        for x, y in [[lo, lo2], [center, center2], [hi, hi2]]:
            assert round(x, 3) == round(y, 3)
