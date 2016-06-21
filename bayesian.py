# author: scott olesen <swo@mit.edu>

'''
Generate myopic Bayesian histories.
'''

import numpy as np
import functools, operator
import scipy.integrate
from fmt_sim import donors as donors_mod
from fmt_sim import simulate

import ctypes
lib = ctypes.CDLL('/Users/scott/lib/fmt_sim/testlib.o')
lib.f.restype = ctypes.c_double
lib.f.argtypes = (ctypes.c_int, ctypes.c_double)

def state_q_new(state):
    n_donors = len(state)
    raw_state = sum([[x, y] for x, y in state], [])
    args = [n_donors] + raw_state

    result = scipy.integrate.nquad(lib.f, [[0, 1]] * 3, args=args)
    return result

def product(xs):
    return functools.reduce(operator.mul, xs)

def state_q_old(state):
    '''returns (value, error)'''
    def integrand(gam, bet, phi):
        eps = gam + bet - gam * bet
        return product([phi * (eps ** si) * ((1.0 - eps) ** fi) + (1.0 - phi) * (bet ** si) * ((1.0 - bet) ** fi) for si, fi in state])

    result = scipy.integrate.nquad(integrand, [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)])
    return result

def with_success(state, i):
    return [(x[0] + 1, x[1]) if j == i else x for j, x in enumerate(state)]

def with_failure(state, i):
    return [(x[0], x[1] + 1) if j == i else x for j, x in enumerate(state)]

def probabilities(state):
    '''posterior probability of donor success'''

    q0 = state_q(state)[0]
    qs = [state_q(with_success(state, i))[0] for i in range(len(state))]
    return [q / q0 for q in qs]

def choice(state):
    return np.argmax(probabilities(state))

def history(donors, n_patients, p_placebo, p_eff):
    quality2p = {0: p_placebo, 1: p_eff}

    for qualities in donors_mod.parse(donors):
        history = ""

        n_donors = len(qualities)
        state = [(0, 0)] * n_donors
        for patient_i in range(n_patients):
            donor_i = choice(state)
            response = np.random.binomial(1, quality2p[qualities[donor_i]])

            if response == 1:
                state = with_success(state, donor_i)
            elif response == 0:
                state = with_failure(state, donor_i)

            history += simulate.show_outcome(response, donor_i)

        yield history
