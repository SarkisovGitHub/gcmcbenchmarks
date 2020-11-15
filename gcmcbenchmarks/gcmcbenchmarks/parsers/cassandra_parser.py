"""Grab all results from cas runs


"""
import glob
import numpy as np
import os
import warnings

from .grab_utils import get_last_ofile


def check_exit(loc):
    """Check that simulation in *loc* exited correctly."""
    # find last .o file
    ofile = get_last_ofile(loc)
    # check for
    with open(ofile, 'r') as f:
        lines = f.readlines()

    if not 'Cassandra simulation complete' in lines[-1]:
        raise ValueError("Simulation did not exit correctly in: {}".format(loc))

    return True


def grab_timeseries(loc, ignore_incomplete=False):
    """Grab mol/uc as a function of time"""
    # figure out which format output this is...
    output = os.path.join(loc, 'CO2_IRMOF.box1.prp1')
    # check results exist
    if not os.path.exists(output):
        output = os.path.join(loc, 'CO2_IRMOF.prp')
        if not os.path.exists(output):
            raise ValueError("Output not found in dir: {}".format(loc))

    # check run ended correctly
    if not ignore_incomplete:
        check_exit(loc)

    # finally grab results
    results = []
    with open(output, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            results.append(float(line.split()[3]))

    return np.array(results) / 8.0  # to mol/uc
