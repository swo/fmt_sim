# author: scott olesen <swo@mit.edu>

'''
Generate and parse donor lists.

Donor lists are newline-separated entries. Each entry consists of a string of 0's and 1's,
one character per donor. "0" means "inefficacious donor"; "1" means "efficacious donor".
'''

import numpy as np

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
