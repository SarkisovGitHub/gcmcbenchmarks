"""
Topology and trajectory reader for MDAnalysis to read DLMonte output

"""
from MDAnalysis.topology.base import TopologyReader
from MDAnalysis.coordinates.base import SingleFrameReader
from MDAnalysis.lib.util import openany
from MDAnalysis.core.AtomGroup import Atom

class DLMParser(TopologyReader):
    format = 'DLM'

    def __init__(self, filename, universe=None):
        self.filename = filename
        self._u = universe

    def parse(self):
        with openany(self.filename) as inf:
            inf.readline()
            levcfg, imcon = map(int, inf.readline().split()[:2])
            # Box info
            if not imcon == 0:
                inf.readline()
                inf.readline()
                inf.readline()

            # Nummol
            inf.readline()

            # Loop over molecules
            resid = 1
            atomid = 0
            atoms = []
            segid = 'SYSTEM'

            line = inf.readline().strip()
            while line:
                if line.startswith('MOLECULE'):
                    resid += 1
                    resname = line.split()[1]
                else:
                    name = line.split()[0]
                    inf.readline()

                    atoms.append(Atom(atomid, name, name, resname, resid,
                                      segid, 1.0, 1.0, universe=self._u))
                    atomid += 1

                line = inf.readline()

        return {'atoms':atoms}
                
            
class DLMReader(SingleFrameReader):
    format = 'DLM'

    def __init__(self, *args, **kwargs):
        self.n_atoms = kwargs.get('n_atoms')
        super(DLMReader, self).__init__(*args, **kwargs)

    def _read_first_frame(self):
        self.ts = ts = self._Timestep(self.n_atoms,
                                      **self._ts_kwargs)

        with openany(self.filename) as inf:
            # title
            inf.readline()
            # levcfg
            inf.readline()
            # box
            inf.readline()
            inf.readline()
            inf.readline()
            # nummol
            inf.readline()
            line = inf.readline()

            atom_iter = 0

            while line:
                if line.strip().startswith('MOL'):
                    line = inf.readline().strip()
                else:
                    ts._pos[atom_iter] = inf.readline().split()[:3]
                    atom_iter += 1
                    line = inf.readline()

            return ts
