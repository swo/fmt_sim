# author: scott olesen <swo@mit.edu>

'''
Analyze trial histories.

Trial histories are newline-separated entries. Each entry consists of a string of pairs
of characters. The first character is a donor ID: 'A' means donor 0, 'B' means 1, etc.
(i.e., donor index + 65 = ASCII value). The second character is 's' (success) or 'f'
(failure).

The placebo trials have one donor marked with character 'P'.
'''

# todo:
# - cache the Fisher's exact test

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
    table = [[treatment_success, treatment_fail, placebo_success, placebo_fail]]
    oddsratio, p_value = scipy.stats.fisher_exact(table, alternative='greater')
    return p_value
