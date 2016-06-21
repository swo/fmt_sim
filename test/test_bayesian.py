# author: scott olesen <swo@mit.edu>

'''
tests for bayesian.py
'''

import pytest
import numpy as np, io
from fmt_sim import bayesian

class TestProduct:
    def test_int(self):
        assert bayesian.product([1, 2, 3]) == 6

    def test_float(self):
        assert bayesian.product([1.0, 2.0, 3.0]) == 6.0


class TestQPython:
    def test_with_f(self):
        history = [1, 2, 3, 4, 5, 0]
        history_s = [2, 2, 3, 4, 5, 0]
        history_f = [1, 3, 3, 4, 5, 0]

        q0, tmp = bayesian.state_q(history)
        qs, tmp = bayesian.state_q(history_s)
        qf, tmp = bayesian.state_q(history_f)

        assert abs((qs + qf) - q0) < 1e-6

    def test_errors_are_small(self):
        history = [1, 2, 3, 4, 5, 0]
        value, error = bayesian.state_q(history)
        assert error < 1e-12

    def test_correct_values(self):
        history = [1, 2, 3, 4, 5, 0]
        value, error = bayesian.state_q(history)
        assert abs(value - 2.116e-5) < 1e-6


class TestProbabilities:
    def test_correct(self):
        history = [1, 2, 3, 4, 5, 0]
        probs = bayesian.probabilities(history)
        assert abs(probs[0] - 0.5247397697356642) < 1e-9
        assert abs(probs[1] - 0.5185752064675783) < 1e-9
        assert abs(probs[2] - 0.7520492574915295) < 1e-9


class TestChoice:
    def test_correct(self):
        history = [1, 2, 3, 4, 5, 0]
        assert bayesian.choice(history) == 2


class TestHistory:
    def test_correct(self):
        donors = ["100", "010"]
        history = list(bayesian.history(donors, 5, 0.0, 1.0))
        assert len(history) == 2
        for line in history:
            assert len(line) == 10
