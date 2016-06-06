# author: scott olesen <swo@mit.edu>

'''
Generate trial histories.

Trial histories are newline-separated entries. Each entry consists of a string of pairs
of characters. The first character is a donor ID: 'A' means donor 0, 'B' means 1, etc.
(i.e., donor index + 65 = ASCII value). The second character is 's' (success) or 'f'
(failure).

The placebo trials have one donor marked with character 'P'.
'''

import numpy as np

def show_outcome(outcome, donor_id):
    if donor_id < 0:
        raise RuntimeError("donor IDs should be nonnegative")

    donor_char = chr(65 + donor_id)
    if outcome == 0:
        return donor_id + "s"
    elif outcome == 1:
        return donor_id + "f"
    else:
        raise RuntimeError("don't recognize outcome '{}'".format(outcome))

def write_placebo(n_trials, n_patients, p_placebo, output):
    for line in placebo_history(n_trials, n_patients, p_placebo):
        output.write(line + "\n")

def placebo_history(n_trials, n_patients, p_placebo):
    for outcomes in np.random.binomial(1, p_placebo, size=(n_trials, n_patients)):
        yield "".join([show_outcome(o, 15) for o in outcomes])

def generate(donors_per_trial, n_trials, ped):
    for donors in np.random.binomial(1, ped, size=(n_trials, donors_per_trial)):
        line = "".join([str(d) for d in donors]) + "\n"
        yield line

def parse(donors):
    for line in donors:
        values = [int(x) for x in line.rstrip()]

        for x in values:
            if x not in [0, 1]:
                raise RuntimeError("malformed donor quality line: {}".format(line.rstrip()))

        yield values

def write(donors_per_trial, n_trials, ped, output):
    for line in generate(donors_per_trial, n_trials, ped):
        output.write(line)
