#!/usr/bin/env python3

from efmaral import align
from cefmaral import ibm_print

import sys, argparse, random, pickle

def main():
    parser = argparse.ArgumentParser(
        description='efmaral: efficient Markov Chain word alignment')
    parser.add_argument(
        '-v', '--verbose', dest='verbose',
        action='store_true', help='Enable verbose output')
    parser.add_argument(
        '--no-lower-case',
        action='store_true', help='Do not lower-case data')
    parser.add_argument(
        '-r', '--reverse', dest='reverse',
        action='store_true', help='Align in the reverse direction')
    parser.add_argument(
        '--null-prior', dest='null_prior', default=0.2, metavar='X',
        type=float, help='Prior probability of NULL alignment')
    parser.add_argument(
        '--lexical-alpha', dest='lex_alpha', default=1e-3, metavar='X',
        type=float, help='Dirichlet prior parameter for lexical distributions')
    parser.add_argument(
        '--null-alpha', dest='null_alpha', default=1e-3, metavar='X',
        type=float, help='Dirichlet prior parameter for NULL word distribution')
    parser.add_argument(
        '--seed', dest='seed', default=None,
        type=int, help='Random seed')
    parser.add_argument(
        '-n', '--samplers', dest='n_samplers', default=2, metavar='N',
        type=int, help='Number of independent samplers')
    parser.add_argument(
        '-m', '--model', dest='model', default=3, metavar='N',
        type=int, help='Model (1 = IBM1, 2 = IBM1+HMM, 3 = IBM1+HMM+fertility)')
    parser.add_argument(
        '--prefix', dest='prefix_len', default=0, metavar='N',
        type=int, help='Length of prefix for stemming (default: no stemming)')
    parser.add_argument(
        '--suffix', dest='suffix_len', default=0, metavar='N',
        type=int, help='Length of suffix for stemming (default: no stemming)')
    parser.add_argument(
        '-l', '--length', dest='length', default=1.0, metavar='X',
        type=float, help='Relative number of sampling iterations')
    parser.add_argument(
        '--output-prob', dest='output_prob', default=None, metavar='FILE',
        type=str, help='File to write probability tables to')
    parser.add_argument(
        '-i', '--input', dest='inputs', type=str, nargs='+',
        metavar='filename',
        help='Input (either one fast_align-format file, or two Europarl-style)')

    args = parser.parse_args()

    if args.verbose:
        from pprint import pprint
        pprint(vars(args), stream=sys.stderr)

    seed = random.randint(0, 0x7ffffff) if args.seed is None else args.seed

    if len(args.inputs) not in (1, 2):
        raise ValueError('Only one or two input files allowed!')

    discretize = args.output_prob is None

    aaa = align(args.inputs, args.n_samplers, args.length,
                args.null_prior, args.lex_alpha, args.null_alpha,
                args.reverse, args.model, args.prefix_len, args.suffix_len,
                seed, discretize, True, lower=not args.no_lower_case)

    print('Writing alignments...', file=sys.stderr)
    if discretize:
        ibm_print(aaa, args.reverse, sys.stdout.fileno())
    else:
        with open(args.output_prob, 'wb') as f:
            pickle.dump(aaa, f, -1)

if __name__ == '__main__': main()

