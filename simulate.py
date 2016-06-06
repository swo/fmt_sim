# author: scott olesen <swo@mit.edu>

'''
Generate trial histories.

Trial histories are newline-separated entries. Each entry consists of a string of pairs
of characters. The first character is a donor ID: 'A' means donor 0, 'B' means 1, etc.
(i.e., donor index + 65 = ASCII value). The second character is 's' (success) or 'f'
(failure).

The placebo trials have one donor marked with character 'P'.
'''

import numpy as np, itertools
from fmt_sim import donors as donors_mod

class Urn:
    '''Polya urn'''
    def __init__(self, n_donors, n_balls0, n_balls_reward, n_balls_penalty, replace=True):
        self.n_donors = n_donors
        self.n_balls0 = n_balls0
        self.n_balls_reward = n_balls_reward
        self.n_balls_penalty = n_balls_penalty
        self.replace = replace

        self.donor_is = list(range(n_donors))

        # initialize urn
        self.counts = [n_balls0] * n_donors

    def choose(self):
        if sum(self.counts) == 0:
            return np.randint(self.n_donors)

        total_balls = sum(self.counts)
        weights = [c / total_balls for c in self.counts]
        donor_i = np.random.choice(self.donor_is, p=weights)

        if not self.replace:
            self.counts[donor_i] -= 1

        return donor_i

    def update(self, response, donor_i):
        if response == 0:
            for donor_j in self.donor_is:
                if donor_j != donor_i:
                    self.counts[donor_j] += self.n_balls_penalty
        elif response == 1:
            self.counts[donor_i] += self.n_balls_reward
        else:
            raise RuntimeError("don't recognize response '{}'".format(response))


def show_outcome(response, donor_id):
    if donor_id < 0:
        raise RuntimeError("donor IDs should be nonnegative")

    donor_char = chr(65 + donor_id)
    if response == 1:
        return donor_char + "s"
    elif response == 0:
        return donor_char + "f"
    else:
        raise RuntimeError("don't recognize outcome '{}'".format(response))

def write_placebo(n_trials, n_patients, p_placebo, output):
    for line in placebo_history(n_trials, n_patients, p_placebo):
        output.write(line + "\n")

def placebo_history(n_trials, n_patients, p_placebo):
    for outcomes in np.random.binomial(1, p_placebo, size=(n_trials, n_patients)):
        # 15 means 'P'
        yield "".join([show_outcome(o, 15) for o in outcomes])

def write_block(donors, n_patients, p_placebo, p_eff, output):
    for line in block_history(donors, n_patients, p_placebo, p_eff):
        output.write(line + "\n")

def block_history(donors, n_patients, p_placebo, p_eff):
    # create a dict that points from patient ID to donor ID
    # compute the dict by counting the patients while cycling through donors
    quality2p = {0: p_placebo, 1: p_eff}

    for qualities in donors_mod.parse(donors):
        history = ""
        for patient_i, donor_i in zip(range(n_patients), itertools.cycle(range(len(qualities)))):
            response = np.random.binomial(1, quality2p[qualities[donor_i]])
            history += show_outcome(response, donor_i)

        yield history

def write_random(donors, n_patients, p_placebo, p_eff, output):
    for line in random_history(donors, n_patients, p_placebo, p_eff, output):
        output.write(line + "\n")

def random_history(donors, n_patients, p_placebo, p_eff):
    quality2p = {0: p_placebo, 1: p_eff}

    for qualities in donors_mod.parse(donors):
        donor_is = np.random.randint(len(qualities), size=n_patients)
        outcomes = [show_outcome(np.random.binomial(1, quality2p[qualities[donor_i]]), donor_i) for donor_i in donor_is]
        yield "".join(outcomes)

def write_urn(donors, n_patients, p_placebo, p_eff, n_balls0, n_balls_reward, n_balls_penalty, no_replace, output):
    for line in urn_history(donors, n_patients, p_placebo, p_eff, n_balls0, n_balls_reward, n_balls_penalty, no_replace):
        output.write(line + "\n")

def urn_history(donors, n_patients, p_placebo, p_eff, n_balls0, n_balls_reward, n_balls_penalty, no_replace):
    quality2p = {0: p_placebo, 1: p_eff}

    for qualities in donors_mod.parse(donors):
        history = ""
        n_donors = len(qualities)

        # initialize urn
        urn = Urn(n_donors, n_balls0, n_balls_reward, n_balls_penalty, not no_replace)
        
        for patient_i in range(n_patients):
            donor_i = urn.choose()
            response = np.random.binomial(1, quality2p[qualities[donor_i]])
            urn.update(response, donor_i)

            history += show_outcome(response, donor_i)

        yield history
