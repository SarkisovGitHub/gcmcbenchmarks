import glob
import numpy as np
import os

from .grab_utils import tail

def check_exit(loc):
    try:
        output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]
    except IndexError:  # if not present, glob will return nothing so IE
        raise ValueError("Output not present in dir: {}".format(loc))
    if not b'Simulation finished' in tail(output, 10):
        raise ValueError("Output didn't exit correctly in dir: {}".format(loc))

    return True

def grab_timeseries(loc, ignore_incomplete=False):
    """Grab timeseries including equilibration time"""
    def _getval1(l):
        #return l
        return float(l.split('adsorption:')[1].split('(avg.')[0])
        #return float(l.split('avg.')[1].split(')')[0])
    def _getval2(l):
        return float(l.split('adsorption:')[1].split('[mol')[0])

    if not ignore_incomplete:
        check_exit(loc)

    output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]

    vals = []
    with open(output, 'r') as f:
        for line in f:
            if line.lstrip(' \t').startswith('absolute adsorption'):
                if 'avg.' in line:
                    vals.append(_getval1(line.lstrip()))
                else:
                    vals.append(_getval2(line.lstrip()))
    return np.array(vals)

def grab_cycle_numbers(loc):
    output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]

    ncyc = []

    def parseline(l):
        return int(l.split('cycle:')[1].split('out of')[0])

    with open(output, 'r') as f:
        for line in f:
            if not line.startswith('Current cycle'):
                continue
            ncyc.append(parseline(line))

    return np.array(ncyc)
                
