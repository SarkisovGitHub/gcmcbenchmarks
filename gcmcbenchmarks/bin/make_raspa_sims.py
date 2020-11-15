#!/usr/bin/env python
"""Make Raspa benchmark simulations

Usage:
  make_raspa_sims.py <setup> <dir> [-n NSTEPS -s NSAMP -c NCOORD] [(-p <pressures>...)]

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
import os
import sys
import shutil

from gcmcbenchmarks.templates import raspa, PRESSURES
from gcmcbenchmarks.templates.raspa import steps_to_cycles


def kPa_to_Pa(pressure):
    return pressure * 1000.0


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_rsp.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0o744)  # rwxr--r-- permissions


def make_sims(pressure_values, setup, destination, options):
    sourcedir = getattr(raspa, setup)
    simdirs = []

    try:
        nsteps = int(options['-n'])
    except ValueError:
        nsteps = map(int, options['-n'].split(','))
    else:
        nsteps = itertools.cycle((nsteps,))

    for p, n in zip(pressure_values, nsteps):
        suffix = 'rsp_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        os.mkdir(newdir)

        for f in ['CO2.def', 'force_field.def', 'framework.def',
                  'IRMOF-1.cif', 'pseudo_atoms.def']:
            shutil.copy(sourcedir[f],
                        os.path.join(newdir, f))

            with open(sourcedir['simulation.input'], 'r') as inf:
                template = inf.read()
            with open(os.path.join(newdir, 'simulation.input'), 'w') as out:
                out.write(template.format(
                    pressure=kPa_to_Pa(p),
                    run_length=steps_to_cycles(n, setup, p),
                    save_freq=steps_to_cycles(int(options['-s']), setup, p),
                    coords_freq=steps_to_cycles(int(options['-c']), setup, p),
                ))
            with open(sourcedir['qsub.sh'], 'r') as inf:
                qsub_template = inf.read()
            with open(os.path.join(newdir, 'qsub.sh'), 'w') as out:
                out.write(qsub_template.format(pressure=p))

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

