#!/usr/bin/env python
"""Create Music benchmark simulations

Usage:
  make_music_sims.py <setup> <dir> [-n NSTEPS -s NSAMP -c NCOORD] [(-p <pressures>...)]

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

from gcmcbenchmarks.templates import music, PRESSURES


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_mus.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0o744)  # rwxr--r-- permissions


def make_sims(pressure_values, setup, destination, options):
    sourcedir = getattr(music, setup)
    simdirs = []  # all simulation directories

    try:
        nsteps = int(options['-n'])
    except ValueError:
        nsteps = map(int, options['-n'].split(','))
    else:
        nsteps = itertools.cycle((nsteps,))

    for p, n in zip(pressure_values, nsteps):
        suffix = 'mus_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        # Make directory for this pressure point
        os.mkdir(newdir)
        # Copy files that don't get modified
        for f in ['atom_atom_all', 'fluid_properties.dat', 'pressure.dat',
                  'intra', 'mol_mol_all', 'setpath']:
            shutil.copy(sourcedir[f],
                        os.path.join(newdir, f))
        # fugacity.dat gets pressure put inside of it
        with open(sourcedir['fugacity.dat'], 'r') as f:
            template = f.read()
        with open(os.path.join(newdir, 'fugacity.dat'), 'w') as out:
            out.write(template.format(
                fugacity=music.FUGACITY[p],
            ))
        # post.ctr needs changing to get the right number of blocks out
        with open(sourcedir['post.ctr'], 'r') as f:
            template = f.read()
        with open(os.path.join(newdir, 'post.ctr'), 'w') as out:
            nblocks = (n // 2) // int(options['-s'])
            out.write(template.format(nblocks=nblocks))
        # gcmc.ctr has runlength options
        with open(sourcedir['gcmc.ctr'], 'r') as f:
            template = f.read()
        with open(os.path.join(newdir, 'gcmc.ctr'), 'w') as out:
            out.write(template.format(
                run_length=n // 2,  # music divided into 2 sims, so halve length
                save_freq=options['-s'],
                coords_freq=options['-c'],
            ))
        with  open(sourcedir['qsub.sh'], 'r') as f:
            template = f.read()
        with open(os.path.join(newdir, 'qsub.sh'), 'w') as out:
            out.write(template.format(pressure=p))

    # These are common across all pressure directories
    for d in ('atoms', 'molecules'):
        newdir = os.path.join(destination, d)
        os.mkdir(newdir)

        flist = getattr(music, d)  # dict of filename : location for this directory
        for fname, floc in flist.items():
            shutil.copy(floc,
                        os.path.join(newdir, fname))

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
