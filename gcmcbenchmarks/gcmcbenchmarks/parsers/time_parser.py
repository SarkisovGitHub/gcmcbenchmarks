"""Parse the results of a timing run

"""
from __future__ import print_function

from dateutil.parser import parse as parsetime
from collections import Counter

import glob
import re
import os
import sys


def _get_prefix(loc):
    """Get the common prefix for simulations in *loc*
    
    Allows working directories (forcefields?) to be ignored by a glob
    """
    # get all subdirectories in loc
    dirs = filter(os.path.isdir,
                  (os.path.join(loc, d)
                   for d in os.listdir(loc))
                  )
    starts = []
    
    # matches 'something/smt_20'
    # grabs 'smt' into group 0
    pattern = re.compile('.+?([a-z]{3})_[0-9]{2,}')
    for d in dirs:
        m = re.match(pattern, d)
        try:
            starts.append(m.groups()[0])
        except AttributeError:
            pass
    # count each time we saw a given token
    c = Counter(starts)
    # return the most common token
    return c.most_common(1)[0][0]


def parse_all_timefiles(d):
    """Return the times elapsed in timing files in directory *d*

    Assumes files called timing* with a format:
     - comment line
     - date call 1
     - date call 2

    Returns
    -------
    a list of timings from that directory
    """
    times = []
    for filename in glob.glob(os.path.join(d, 'timing*')):
        try:
            delta = parse_timefile(filename)
        except ValueError as e:
            pass
            #print('Failed for file: {}\n{}'.format(filename, e))
        else:
            if delta > 60:  # ignore too small values
                times.append(delta)
    return times

def parse_timefile(fn):
    """Parse a single timing file

    Assumes files with the format:
     - comment line
     - date call 1
     - date call 2
    """
    with open(fn, 'r') as inp:
        t1, t2 = map(parsetime, inp.readlines()[1:])

    return (t2 - t1).total_seconds()


def parse_cpuinfo(d):
    """Grab the results of a cpu query from directory *d*

    Returns
    -------
    string of the CPU info
    """
    # files will be result of cat /proc/cpuinfo > cpuinfo.$pressure
    filename = glob.glob(os.path.join(d, 'cpuinfo*'))[0]

    for line in open(filename, 'r'):
        if line.startswith('model name'):
            break
    # this line will look something like:
    # "model name : Intel 1234\n"
    return line.split(':')[1].strip()


def grab_times(loc):
    """Grab all timings from directories starting with *prefix*

    Returns
    -------
    list of timings
    """
    timings = []

    for d in glob.glob('{}_*'.format(os.path.join(loc, _get_prefix(loc)))):
        try:
            times = parse_all_timefiles(d)
            cpuinfo = parse_cpuinfo(d)
        except IndexError:
            continue
        else:
            timings.append((d, times, cpuinfo))
    return timings

def get_pressure(fn):
    """Grab pressure from filename like 'dlm_timing/dlm_10'"""
    return int(fn.split('_')[-1])

def sort_times(a, b):
    """Sort *a* and *b* according to order of *a*"""
    return zip(*sorted(zip(a, b), key=lambda x: x[0]))

def get_times(loc):
    """Grab all timing results from *loc*
    
    Returns: pressures, times
    """
    times = grab_times(loc)
    
    pressures = [get_pressure(t[0]) for t in times]
    times = [map(int, t[1]) for t in times]
    
    return sort_times(pressures, times)



        
