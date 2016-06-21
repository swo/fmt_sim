# author: scott olesen <swo@mit.edu>

'''
Generate myopic Bayesian histories.
'''

import numpy as np
import functools, operator, os.path, ctypes
import scipy.integrate
from fmt_sim import donors as donors_mod, simulate

class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, lst):
        args = tuple(lst)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(lst)

            if sum(args) < 10:
                self.cache[args] = value

            return value

@memoized
def state_q_c(state):
    n_donors = len(state) // 2
    args = [n_donors] + state

    result = scipy.integrate.nquad(lib.f, [[0, 1]] * 3, args=args)
    return result

def product(xs):
    return functools.reduce(operator.mul, xs)

@memoized
def state_q_python(state):
    '''returns (value, error)'''
    def integrand(gam, bet, phi):
        eps = gam + bet - gam * bet
        return product([phi * (eps ** si) * ((1.0 - eps) ** fi) + (1.0 - phi) * (bet ** si) * ((1.0 - bet) ** fi) for si, fi in zip(*[iter(state)] * 2)])

    result = scipy.integrate.nquad(integrand, [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)])
    return result

library_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bayesian_lib.o')
if os.path.exists(library_fn):
    lib = ctypes.CDLL(library_fn)
    lib.f.restype = ctypes.c_double
    lib.f.argtypes = (ctypes.c_int, ctypes.c_double)
    state_q = state_q_c
else:
    state_q = state_q_python

def probabilities(state):
    '''posterior probability of donor success'''

    q0 = state_q(state)[0]
    qs = []

    for i in range(len(state) // 2):
        new_state = list(state)
        new_state[i * 2] += 1
        qs.append(state_q(new_state)[0])

    return [q / q0 for q in qs]

def choice(state):
    return np.argmax(probabilities(state))

def history(donors, n_patients, p_placebo, p_eff):
    quality2p = {0: p_placebo, 1: p_eff}

    for qualities in donors_mod.parse(donors):
        history = ""

        n_donors = len(qualities)
        state = [0] * (2 * n_donors)
        for patient_i in range(n_patients):
            donor_i = choice(state)
            response = np.random.binomial(1, quality2p[qualities[donor_i]])

            state[donor_i * 2 + (1 - response)] += 1

            history += simulate.show_outcome(response, donor_i)

        yield history
