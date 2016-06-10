# author: scott olesen <swo@mit.edu>

'''
Analyze trial histories.

Trial histories are newline-separated entries. Each entry consists of a string of pairs
of characters. The first character is a donor ID: 'A' means donor 0, 'B' means 1, etc.
(i.e., donor index + 65 = ASCII value). The second character is 's' (success) or 'f'
(failure).

The placebo trials have one donor marked with character 'P'.
'''

import numpy as np
import scipy.stats

class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result

def clopper_pearson(x, n, conf=0.95):
    '''
    "Exact" binomial confidence intervals 

    x= # successes
    n= # trials
    conf= confidence interval
    '''

    alpha = 1.0 - conf
    lo = scipy.stats.beta.ppf(alpha / 2, x, n - x + 1)
    hi = scipy.stats.beta.ppf(1.0 - alpha / 2, x + 1, n - x)
    return (lo, hi)

@memoize
def fisher_exact_p(treatment_success, placebo_success, arm_size):
    '''
    Fisher's exact test p-value when the number of patients in the two arms is the same
    and the alternative hypothesis is "greater rate in treatment arm"
    '''

    treatment_fail = arm_size - treatment_success
    placebo_fail = arm_size - placebo_success
    table = [[treatment_success, treatment_fail], [placebo_success, placebo_fail]]
    oddsratio, p_value = scipy.stats.fisher_exact(table, alternative='greater')
    return p_value

def parse_history_line(line):
    if not set(line.rstrip()[1::2]) <= {'s', 'f'}:
        raise RuntimeError("history line '{}' does not have appropriate 's' and 'f' markers".format(line.rstrip()))

    if not all([ord(c) >= 65 for c in line.rstrip()[::2]]):
        raise RuntimeError("history line '{}' have inappropriate donor IDs".format(line.rstrip()))

    n_successes = line.count('s')
    n_total = len(line.rstrip()) // 2
    return n_successes, n_total

def power(treatment_history, placebo_history, conf=0.95):
    total_trials = 0
    significant_trials = 0
    for tx_line, pl_line in zip(treatment_history, placebo_history):
        n_tx_succ, n_tx_total = parse_history_line(tx_line)
        n_pl_succ, n_pl_total = parse_history_line(pl_line)
        assert n_tx_total == n_pl_total
        p = fisher_exact_p(n_tx_succ, n_pl_succ, n_tx_total)

        if p < 0.05:
            significant_trials += 1

        total_trials += 1

    if total_trials == 0:
        raise RuntimeError("can't compute power on empty file")

    center = significant_trials / total_trials
    lo, hi = clopper_pearson(significant_trials, total_trials, conf=conf)
    return (lo, center, hi)

def write_power(treatment_history, placebo_history, output):
    lo, center, hi = power(treatment_history, placebo_history)
    print("\t".join([str(x) for x in [lo, center, hi]]), file=output)
