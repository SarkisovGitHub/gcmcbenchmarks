#!/usr/bin/env python
"""Make many DLMonte simulation directories

Usage:
  make_dlm_sims.py <setup> <dir> [-n NSTEPS -s NSAMP -c NCOORD] [(-p <pressures>...)]

Options:
  -h --help
  -v --version
  -n N                Number of steps, can also be , delimited list. [default: 11000000]
  -s N                Number of steps between samples [default: 1000]
  -c N                Number of steps between saving coordinates [default: 100000]
  -p                  Specify manual pressure points
  <pressures>...      Pressure points [default: 5 10 20 30 40 50 60 70]

"""
from __future__ import division

from docopt import docopt
import itertools
import sys
import os
import shutil

from gcmcbenchmarks.templates import dlmonte, PRESSURES


def kPa_to_kAtm(p):
    """Convert kPa to kAtm (dlmonte units)"""
    return p / 101325


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_dlm.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0o744)  # rwxr--r-- permissions


def make_sims(pressure_values, setup, destination, options):
    """Make many simulation directories

    pressure_values - list of pressues in kPa to make simulations for
    setup - directory where template files can be found
    destination - directory to place new simulation files in
    options - dict from docopt of simulation settings options
    """
    sourcedir = getattr(dlmonte, setup)  # dict of filename: filepath
    simdirs = []

    try:
        nsteps = int(options['-n'])
    except ValueError:
        nsteps = map(int, options['-n'].split(','))
    else:
        nsteps = itertools.cycle((nsteps,))

    for p, n in zip(pressure_values, nsteps):
        suffix = 'dlm_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        os.mkdir(newdir)

        # Files that don't change between runs
        for f in ['FIELD', 'CONFIG']:
            shutil.copy(sourcedir[f],
                        os.path.join(newdir, f))
        # Files that need customising for this pressure
        with open(sourcedir['CONTROL'], 'r') as f:
            template = f.read()
        with open(os.path.join(newdir, 'CONTROL'), 'w') as out:
            out.write(template.format(
                pressure=kPa_to_kAtm(p),
                run_length=n,
                save_freq=int(options['-s']),
                coords_freq=int(options['-c']),
            ))
        with  open(sourcedir['qsub.sh'], 'r') as f:
            qsub_template = f.read()
        with open(os.path.join(newdir, 'qsub.sh'), 'w') as out:
            out.write(qsub_template.format(pressure=p))

    # Make convenience script for starting jobs
    make_qsubmany(simdirs, destination)


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['-p']:
        pressures = [int(p) for p in args['<pressures>']]
    else:
        pressures = PRESSURES

    destination = args['<dir>']

    if not os.path.exists(os.path.join(os.getcwd(), destination)):
        os.mkdir(destination)
    elif not os.path.isdir(os.path.join(os.getcwd(), destination)):
        raise SystemExit

    make_sims(pressures, args['<setup>'], destination, args)
