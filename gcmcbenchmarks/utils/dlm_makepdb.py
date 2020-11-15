"""Convert a DL Monte REVCON file to a PDB"""
import MDAnalysis as mda
from dlm_parser import (
    DLMParser,
    DLMReader
)

box = [51.664] * 3 + [90.0] * 3

u = mda.Universe('REVCON.000', format='DLM')
u.dimensions = box
u.atoms.pack_into_box()

u.atoms.write('out.pdb')
