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
