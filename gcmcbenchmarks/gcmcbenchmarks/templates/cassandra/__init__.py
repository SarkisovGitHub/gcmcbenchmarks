from functools import partial
import os
from pkg_resources import resource_filename

_rf = partial(resource_filename, __name__)

# calculated in FugacityCalc notebook
# in kJ/mol
CHEMPOTS = {
    5: -31.7610,
    10: -30.5636,
    20: -29.3675,
    30: -28.6689,
    40: -28.1740,
    50: -27.7907,
    60: -27.4780,
    70: -27.2141,
}

_FILES = ['CO2.ff', 'CO2.mcf', 'CO2.pdb',
          'IRMOF.ff', 'IRMOF.mcf', 'IRMOF.pdb', 'IRMOF.xyz',
          'CO2_IRMOF.inp', 'qsub.sh']
# Files found in species2/frag1/
_FRAG1 = ['frag1.dat']
# Files found in species2/fragments
_FRAGMENTS = ['frag_1_1.car', 'frag_1_1.xyz', 'species2_mcf_gen.chk', 'species2_mcf_gen.log',
              'frag_1_1.mcf', 'molecule.pdb', 'species2_mcf_gen.inp']

setup1 = {f: _rf(os.path.join('cas_setup1', f)) for f in _FILES}
setup1['frag1'] = {'frag1.dat': _rf('cas_setup1/species2/frag1/frag1.dat')}
setup1['fragments'] = {f: _rf(os.path.join('cas_setup1/species2/fragments', f))
                      for f in _FRAGMENTS}

setup2 = {f: _rf(os.path.join('cas_setup2', f)) for f in _FILES}
setup2['frag1'] = {'frag1.dat': _rf('cas_setup2/species2/frag1/frag1.dat')}
setup2['fragments'] = {f: _rf(os.path.join('cas_setup2/species2/fragments', f))
                      for f in _FRAGMENTS}

setup3 = {f: _rf(os.path.join('cas_setup3', f)) for f in _FILES}
setup3['frag1'] = {'frag1.dat': _rf('cas_setup3/species2/frag1/frag1.dat')}
setup3['fragments'] = {f: _rf(os.path.join('cas_setup3/species2/fragments', f))
                      for f in _FRAGMENTS}

