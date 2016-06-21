#!/usr/bin/env python3
#
# author: scott olesen <swo@mit.edu>

'''
command-line interface
'''

import argparse, sys
import donors, simulate, analyze

def parse_args(args=None):
    parser = argparse.ArgumentParser(description='simulate and analyze FMT trials')
    cmd_parsers = parser.add_subparsers(title='commands', metavar='cmd')

    p = cmd_parsers.add_parser('donors', help='generate donor lists')
    p.add_argument('donors_per_trial', type=int)
    p.add_argument('n_trials', type=int)
    p.add_argument('ped', type=float, help='prevalence of efficacious donors')
    p.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='donor list')
    p.set_defaults(func=donors.write)

    p = cmd_parsers.add_parser('simulate', help='simulate trials')
    sp = p.add_subparsers()

    p = sp.add_parser('placebo', help='simulate "one-donor" placebo group')
    p.add_argument('n_trials', type=int)
    p.add_argument('n_patients', type=int)
    p.add_argument('p_placebo', type=float, help='placebo response rate')
    p.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='trial history')
    p.set_defaults(func=simulate.write_placebo)

    p = sp.add_parser('block', help='assign donors to patients in blocks')
    p.add_argument('donors', type=argparse.FileType('r'), help='donor list')
    p.add_argument('n_patients', type=int)
    p.add_argument('p_placebo', type=float, help='placebo response rate')
    p.add_argument('p_eff', type=float, help='efficacious treatment response rate')
    p.add_argument('--n_donors', type=int, default=None, help='specify a limited number of donors? [default: use all donors]')
    p.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='trial history')
    p.set_defaults(func=simulate.write_block)

    p = sp.add_parser('random', help='randomly assign donors')
    p.add_argument('donors', type=argparse.FileType('r'), help='donor list')
    p.add_argument('n_patients', type=int)
    p.add_argument('p_placebo', type=float, help='placebo response rate')
    p.add_argument('p_eff', type=float, help='efficacious treatment response rate')
    p.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='trial history')
    p.set_defaults(func=simulate.write_random)

    p = sp.add_parser('urn', help='assign donors with a Polya urn')
    p.add_argument('donors', type=argparse.FileType('r'), help='donor list')
    p.add_argument('n_patients', type=int)
    p.add_argument('p_placebo', type=float, help='placebo response rate')
    p.add_argument('p_eff', type=float, help='efficacious treatment response rate')
    p.add_argument('n_balls0', type=int, help='initial number of balls per donor')
    p.add_argument('n_balls_reward', type=int, help='number of balls to give to a donor after a success')
    p.add_argument('n_balls_penalty', type=int, help='number of balls to give to other donors after a failure')
    p.add_argument('--no_replace', action='store_true', help='do not replace drawn ball?')
    p.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='trial history')
    p.set_defaults(func=simulate.write_urn)

    p = sp.add_parser('bayesian', help='assign donors with myopic Bayesian algorithm (flat prior)')
    p.add_argument('donors', type=argparse.FileType('r'), help='donor list')
    p.add_argument('n_patients', type=int)
    p.add_argument('p_placebo', type=float, help='placebo response rate')
    p.add_argument('p_eff', type=float, help='efficacious treatment response rate')
    p.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='trial history')
    p.set_defaults(func=simulate.write_bayesian)

    p = cmd_parsers.add_parser('power', help='power')
    p.add_argument('treatment_history', type=argparse.FileType('r'), help='trial history from treatment arm')
    p.add_argument('placebo_history', type=argparse.FileType('r'), help='trial history from placebo arm')
    p.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='power report')
    p.set_defaults(func=analyze.write_power)

    args = parser.parse_args(args)
    opts = vars(args)

    func = opts.pop('func')

    return func, opts

if __name__ == '__main__':
    func, opts = parse_args()
    func(**opts)
