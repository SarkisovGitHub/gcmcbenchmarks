from functools import partial
import os
from pkg_resources import resource_filename

_rf = partial(resource_filename, __name__)

_FILES = ['qsub.sh', 'towhee_coords', 'towhee_ff_CUSTOM', 'towhee_input']

setup1 = {f: _rf(os.path.join('twh_setup1', f)) for f in _FILES}
setup2 = {f: _rf(os.path.join('twh_setup2', f)) for f in _FILES}
setup3 = {f: _rf(os.path.join('twh_setup3', f)) for f in _FILES}

# chemical potentials calculated in PREoS notebook
CHEMPOTS = {5:-3819.9691,
            10:-3675.9523,
            20:-3532.0937,
            30:-3448.0733,
            40:-3388.5522,
            50:-3342.4555,
            60:-3304.8501,
            70:-3273.1046,
}
