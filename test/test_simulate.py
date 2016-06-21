# author: scott olesen <swo@mit.edu>

'''
tests for donors.py
'''

import pytest
import numpy as np, io
from fmt_sim import simulate

@pytest.fixture
def urn():
    return simulate.Urn(4, 1, 3, 2)

class TestUrn:
    def test_initialization(self, urn):
        assert urn.counts == [1, 1, 1, 1]

    def test_choose(self, urn):
        assert urn.choose() in [0, 1, 2, 3]

    def test_empty_choose(self):
        assert simulate.Urn(3, 0, 0, 0).choose() in [0, 1, 2]

    def test_choose_deterministic(self):
        urn = simulate.Urn(4, 0, 3, 2)
        urn.update(1, 2)
        assert urn.choose() == 2

    def test_update_success(self, urn):
        urn.update(1, 0)
        assert urn.counts == [4, 1, 1, 1]

    def test_update_fail(self, urn):
        urn.update(0, 2)
        assert urn.counts == [3, 3, 1, 3]

    def test_no_replace(self):
        urn = simulate.Urn(4, 1, 3, 2, replace=False)
        urn.choose()
        assert(sum(urn.counts) == 3)


class TestShowOutcome:
    def test_correct(self):
        assert simulate.show_outcome(0, 0) == "Af"
        assert simulate.show_outcome(1, 1) == "Bs"

    def test_fail(self):
        with pytest.raises(RuntimeError):
            simulate.show_outcome('a', 0)


class TestPlaceboHistory:
    def test_correct_all(self):
        history = list(simulate.placebo_history(100, 10, 1.0))
        assert len(history) == 100
        for line in history:
            assert line == "Ps" * 10

    def test_correct_none(self):
        history = list(simulate.placebo_history(100, 10, 0.0))
        assert len(history) == 100
        for line in history:
            assert line == "Pf" * 10

    def test_correct_some(self):
        history = list(simulate.placebo_history(100, 10, 0.5))
        assert len(history) == 100
        for line in history:
            assert len(line) == 20
            assert line.count('P') == 10


class TestPlaceboWrite:
    def test_correct(self):
        f = io.StringIO()
        simulate.write_placebo(10, 5, 0.5, f)
        f.seek(0)
        lines = [l.rstrip() for l in f.readlines()]
        assert len(lines) == 10

        for line in lines:
            assert len(line) == 10
            assert set(line[::2]) == {'P'}
            assert set(line[1::2]) <= {'s', 'f'}


class TestBlockHistory:
    def test_correct(self):
        # donor A is totally efficacious; B and C are totally useless
        donors = ["100"]
        history = list(simulate.block_history(donors, 8, 0.0, 1.0))
        assert len(history) == 1
        assert history[0] == "AsBfCfAsBfCfAsBf"

    def test_limited(self):
        # donor A is totally efficacious; B and C are totally useless
        donors = ["100"]
        history = list(simulate.block_history(donors, 8, 0.0, 1.0, n_donors=2))
        assert len(history) == 1
        assert history[0] == "AsBfAsBfAsBfAsBf"

    def test_limited_error(self):
        donors = ["100"]
        with pytest.raises(RuntimeError):
            list(simulate.block_history(donors, 8, 0.0, 1.0, n_donors=10))


class TestBlockWrite:
    def test_correct(self):
        f = io.StringIO()
        simulate.write_block(["010"] * 10, 5, 1.0, 0.0, f)
        f.seek(0)
        lines = [l.rstrip() for l in f.readlines()]
        assert len(lines) == 10

        for line in lines:
            assert line == "AsBfCsAsBf"


class TestRandomWrite:
    def test_correct(self):
        f = io.StringIO()
        simulate.write_random(["010"] * 10, 5, 1.0, 0.0, f)
        f.seek(0)
        lines = [l.rstrip() for l in f.readlines()]
        assert len(lines) == 10

        for line in lines:
            assert len(line) == 10
            assert set(line[::2]) <= {'A', 'B', 'C'}
            assert set(line[1::2]) <= {'s', 'f'}


class TestRandomHistory:
    def test_correct(self):
        donors = ["".join(np.random.choice(['0', '1'], size=3)) for i in range(20)]
        history = list(simulate.random_history(donors, 8, 0.0, 1.0))
        assert len(history) == 20
        for h in history:
            assert set(h[::2]) <= {'A', 'B', 'C'}
            assert set(h[1::2]) <= {'s', 'f'}


class TestUrnHistory:
    def test_correct(self):
        donors = ["".join(np.random.choice(['0', '1'], size=3)) for i in range(20)]
        history = list(simulate.urn_history(donors, 8, 0.25, 0.5, 1, 3, 2, no_replace=False))
        assert len(history) == 20
        for h in history:
            assert set(h[::2]) <= {'A', 'B', 'C'}
            assert set(h[1::2]) <= {'s', 'f'}


class TestBayesianHistory:
    def test_correct(self):
        f = io.StringIO()
        simulate.write_bayesian(["010"] * 2, 5, 1.0, 0.0, f)
        f.seek(0)
        lines = [l.rstrip() for l in f.readlines()]
        assert len(lines) == 2

        for line in lines:
            assert len(line) == 10
            assert set(line[::2]) <= {'A', 'B', 'C'}
            assert set(line[1::2]) <= {'s', 'f'}
