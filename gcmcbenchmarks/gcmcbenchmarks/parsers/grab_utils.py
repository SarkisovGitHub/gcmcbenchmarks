"""Common functions for results grabbing

"""
import functools
import glob
import os
import re
import subprocess

# regex match lazy anything, .o, then numerical chars
_O_PATTERN = re.compile('^.+?\.o[0-9]+$')
_O_MATCH = functools.partial(re.match, _O_PATTERN)


def _getnum(fname):
    """Return number from ofile name"""
    return int(fname.split('.o')[1])


def get_last_ofile(loc):
    """Return name of last o file"""
    # remove tilde files
    ofiles = filter(_O_MATCH,
                    glob.glob(os.path.join(loc, '*.o*')))

    return max(ofiles, key=_getnum)

def tail(fn, n):
    """Similar to 'tail -n *n* *fn*'

    Parameters
    ----------
    fn : str
      Path to file to tail
    n : int
      Number of lines to return

    Returns
    -------
    A bytes string representing the output.  Use split to get lines.
    """
    p = subprocess.Popen(['tail', '-n', str(n), fn],
                         stdout=subprocess.PIPE)
    p.wait()  # allow subprocess to finish
    stdout, stderr = p.communicate()

    return stdout
