from functools import partial
import os
from pkg_resources import resource_filename

from .conversions import cycles_to_steps, steps_to_cycles, find_completed_steps

_rf = partial(resource_filename, __name__)

_FILES = ['CO2.def', 'force_field.def', 'framework.def', 'IRMOF-1.cif', 'pseudo_atoms.def',
          'simulation.input', 'qsub.sh']

setup1 = {f: _rf(os.path.join('rsp_setup1', f)) for f in _FILES}
setup2 = {f: _rf(os.path.join('rsp_setup2', f)) for f in _FILES}
setup3 = {f: _rf(os.path.join('rsp_setup3', f)) for f in _FILES}

setup1_withgrid = {f: _rf(os.path.join('rsp_setup1_withgrid', f)) for f in _FILES}
setup2_withgrid = {f: _rf(os.path.join('rsp_setup2_withgrid', f)) for f in _FILES}
setup3_withgrid = {f: _rf(os.path.join('rsp_setup3_withgrid', f)) for f in _FILES}
