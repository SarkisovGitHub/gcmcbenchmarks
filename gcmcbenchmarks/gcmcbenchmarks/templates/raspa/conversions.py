"""Raspa uses cycles not steps

1 cycle = 1 move per molecule

This has functions to convert between moves and cycles for the case studies.

Requires you to know the isotherm a priori..
"""
import glob
import os

from gcmcbenchmarks.parsers.grab_utils import tail

# Average number of molecules at a given pressure (ie the result)
# Used to translate between steps and cycles for benchmarking
#
# This changes depending on which setup is done, so dict for each
_NMOL_setup1 = {  # LJ only
    5 : 4.09 * 8,  # result in mol/uc then *8 because 2x2x2 sim box
    10 : 8.70 * 8,
    20 : 18.57 * 8,
    30 : 30.84 * 8,
    40 : 48.06 * 8,
    50 : 79.01 * 8,
    60 : 115.95 * 8,
    70 : 133.53 * 8,
}
_NMOL_setup2 = {  # LJ and FF electrostatics
    5 : 4.26 * 8,
    10 : 9.39 * 8,
    20 : 25.44 * 8,
    30 : 179.30 * 8,
    40 : 185.95 * 8,
    50 : 189.64 * 8,
    60 : 193.60 * 8,
    70 : 194.98 * 8,
}
_NMOL_setup3 = {  # LJ and all electrostatics
    5 : 7.66 * 8,
    10 : 16.39 * 8,
    20 : 167.60 * 8,
    30 : 183.32 * 8,
    40 : 190.16 * 8,
    50 : 193.94 * 8,
    60 : 196.35 * 8,
    70 : 198.15 * 8,
}
NMOL = {
    'setup1':_NMOL_setup1,
    'setup2':_NMOL_setup2,
    'setup3':_NMOL_setup3,
}

def steps_to_cycles(steps, setup, pressure):
    """Translate a number of steps to cycles

    Parameters
    ----------
    Steps
      Number of Monte Carlo moves desired
    setup
      System conditions [setup1/setup2/setup3]
    pressure
      Pressure in kPa

    Returns
    -------
    number of cycles
    """
    # select the pressure->nmol dict to use
    trans = NMOL[setup[:6]]

    # need integer number of cycles, minimum of 1
    return max(int(steps / trans[pressure]), 1)


def cycles_to_steps(cycles, setup, pressure):
    """Translate a number of cycles to steps

    Parameters
    ----------
    Cycles
      Number of Monte Carlo cycles
    setup
      [setup1/setup2/setup3]
    pressure
      pressure in kPa
    """
    trans = NMOL[setup[:6]]

    return int(cycles * trans[pressure])


def find_completed_steps(loc, setup, pressure):
    """Find the number of complete steps an incomplete Raspa sim finished

    Parameters
    ----------
    loc
      Where the simulation took place (root folder of sim)
    setup
      setup1/setup2/setup3
    pressure : int
      pressure in kPa

    Returns
    -------
    number of MC steps
    """
    output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]

    data = tail(output, 12)
        
    start = data.find('cycle:') + 6  # where this string ends
    end = data[start:].find('out of') + start

    return cycles_to_steps(int(data[start:end]), setup, pressure)
