from functools import partial
import os
from pkg_resources import resource_filename

_rf = partial(resource_filename, __name__)

_FILES = ['atom_atom_all', 'fluid_properties.dat', 'fugacity.dat', 'gcmc.ctr',
          'intra', 'mol_mol_all', 'post.ctr', 'pressure.dat', 'qsub.sh', 'setpath']

_MOL_FILES = ['Carbon_M.mol', 'CO2.mol', 'IRMOF1.in', 'IRMOF1.mol', 'IRMOF1.mol_RASPA',
              'IRMOF1_MUSIC.mol', 'IRMOF1.xyz', 'Oxygen_M.mol', 'Probe.mol']
_ATOM_FILES = ['Carbon.atm', 'Carbon_CO2.atm', 'Hydrogen.atm',
               'Oxygen.atm', 'Oxygen_CO2.atm', 'Probe.atm',
               'Zinc.atm']
_PMAPS_FILES = ['atom_atom_coul', 'atom_atom_lj', 'intra_C', 'intra_el',
                'intra_O', 'mapgen_C.ctr', 'mapgen_el.ctr', 'mapgen_O.ctr',
                'mol_mol_C', 'mol_mol_el', 'mol_mol_O', 'script_map.pbs',
                'script.pbs', 'setpath', 'sili.xyz']

# these are common across all setups
molecules = {f: _rf(os.path.join('molecules', f)) for f in _MOL_FILES}
atoms = {f: _rf(os.path.join('atoms', f)) for f in _ATOM_FILES}
pmaps_krista = {}

setup1 = {f: _rf(os.path.join('mus_setup1', f)) for f in _FILES}
setup2 = {f: _rf(os.path.join('mus_setup2', f)) for f in _FILES}
setup3 = {f: _rf(os.path.join('mus_setup3', f)) for f in _FILES}

setup1_withgrid = {f: _rf(os.path.join('mus_setup1_withgrid', f)) for f in _FILES}
setup2_withgrid = {f: _rf(os.path.join('mus_setup2_withgrid', f)) for f in _FILES}
setup3_withgrid = {f: _rf(os.path.join('mus_setup3_withgrid', f)) for f in _FILES}


FUGACITY = {
    5: 4.996, 10: 9.985, 20: 19.94, 30: 29.86,
    40: 39.76, 50: 49.62, 60: 59.46, 70: 69.26
}
