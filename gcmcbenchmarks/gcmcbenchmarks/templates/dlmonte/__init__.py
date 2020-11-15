from functools import partial
import os
from pkg_resources import resource_filename

_rf = partial(resource_filename, __name__)

# All files in a dlmonte simulation
_FILES = ['CONTROL', 'FIELD', 'CONFIG', 'qsub.sh']

# For each setup, a dict of filename to filepath
setup1 = {f: _rf(os.path.join('dlm_setup1', f)) for f in _FILES}
setup2 = {f: _rf(os.path.join('dlm_setup2', f)) for f in _FILES}
setup3 = {f: _rf(os.path.join('dlm_setup3', f)) for f in _FILES}


