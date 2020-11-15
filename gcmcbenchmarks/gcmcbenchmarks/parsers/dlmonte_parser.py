"""Grab all results from dlm runs

for each dlm_* directory:
   check OUTPUT exists?
   check OUTPUT exited correctly?
   read the results
"""
import numpy as np
import os

from .grab_utils import tail


def check_exit(loc):
    """Check that simulation in *loc* exited correctly."""
    output = os.path.join(loc, 'OUTPUT.000')

    # check results have been generated
    if not os.path.exists(output):
        raise ValueError("Output not present in dir: {}".format(loc))
    # check results ended correctly
    if not b'normal exit' in tail(output, 5):
        raise ValueError("Output didn't exit correct in dir: {}".format(loc))

    return True


def grab_timeseries(loc, ignore_incomplete=False):
    if not ignore_incomplete:
        check_exit(loc)

    output = os.path.join(loc, 'OUTPUT.000')

    # grab lines beginning with ' CO2'
    results = []
    with open(output, 'r') as f:
        for line in f:
            if line.startswith(' CO2'):
                try:
                    results.append(float(line.split()[1]))
                except (ValueError, IndexError):
                    pass
    # last result is an average, discard it
    return np.array(results[:-1]) / 8.0  # to mol/uc
