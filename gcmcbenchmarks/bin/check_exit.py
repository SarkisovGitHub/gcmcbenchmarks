#!/usr/bin/env python
"""Check the exit status of many simulations

Usage:
  check_exit <dir> [-p <P>]

Options:
  -p P, --program P  Specify which program, otherwise guess
"""
from __future__ import print_function

from docopt import docopt
import os
import re

from gcmcbenchmarks import parsers

CHECKERS = {
    'cas':parsers.cassandra_parser.check_exit,
    'dlm':parsers.dlmonte_parser.check_exit,
    'rsp':parsers.raspa_parser.check_exit,
    'twh':parsers.towhee_parser.check_exit,
    'mus':parsers.music_parser.check_exit,
}

PROGS = {
    'c':'cas',
    'd':'dlm',
    'r':'rsp',
    't':'twh',
    'm':'mus',
}

# regex to match 'somedir/mus_50' and capture '50' as first group
SUBDIR_PAT = re.compile('.*?\w{3}_(\d{1,2})$')


def guess_program(loc):
    # try and guess what format this is
    for part in ['dlm', 'rsp', 'twh', 'mus']:
        if part in loc:
            return part
    else:
        return 'cas'


if __name__ == '__main__':
    args = docopt(__doc__)

    d = args['<dir>']

    # figure out what program this is
    if not args['--program']:
        program = guess_program(d)
    else:
        program = args['--program']
    # convert to shorthand
    program = PROGS[program[0].lower()]
    # grab appropriate function
    checker = CHECKERS[program]

    # find all subdirectories
    subdirs = {}
    for loc in os.listdir(d):
        m = re.match(SUBDIR_PAT, loc)
        if not m:
            continue
        p = int(m.groups()[0])
        subdirs[p] = loc

    # sort subdirs
    subdirs = sorted(subdirs.items())

    # for each subdir, give true/false on if finished
    for _, loc in subdirs:
        try:
            finished = checker(os.path.join(d, loc))
        except ValueError:
            finished = False
        print("{} : {}".format(loc, finished))
