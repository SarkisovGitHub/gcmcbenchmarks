"""Towhee basic configuration writer

"""
from __future__ import print_function

def is_central(atom, improper):
    """Returns if an atom in central in an improper

    Parameters
    ----------
    atom : MDAnalysis Atom
      The atom in question
    improper : MDAnalysis ImproperTorsions
      The improper torsion in question
    """
    other_atoms = (other for other in improper
                   if not other == atom)
    return all(other in atom.bonded_atoms
               for other in other_atoms)


def write_basic(molecule, **kwargs):
    """Write the basic input section

    Parameters
    ----------
    molecule : AtomGroup
      MDAnalysis AtomGroup of the molecule you wish to output

    Keywords
    --------
    forcefield : str
      the forcefield to use, must correspond to one known to Towhee
    charge_assignment : str
      the method for writing out charges.
      Must be one of:
        - 'bond increment'
        - 'manual'
        - 'none'

    Notes
    -----
    Missing parameters are marked with a '##'

    Source:
    http://towhee.sourceforge.net/inpstyle/inpstyle_2.html
    """
    try:
        forcefield = kwargs['forcefield']
    except KeyError:
        print("Missing 'forcefield' keyword")
        forcefield = '##FORCEFIELD'
    try:
        charge_assignment = kwargs['charge_assignment']
    except KeyError:
        print("Missing 'charge_assignment' keyword")
        print("-- Will guess as 'none'")
        charge_assignment = 'none'
    finally:
        withcharge = charge_assignment == 'manual'

    # Decide unit output format
    if withcharge:
        outformat = ("unit ntype qqatom\n"
                     "  {unit} '{atom.name}' {atom.charge}\n")
    else:
        outformat = ("unit ntype\n"
                     "  {unit} '{atom.name}'\n")

    with open('basic.out', 'w') as out:
        # Write out settings of basic input
        out.write("input_style\n'basic connectivity map'\n")
        out.write("nunit \n{}\n".format(len(molecule)))
        out.write("nmaxcbmc \n{}\n".format(len(molecule)))
        out.write("lpdbnames \n.FALSE.\n")
        out.write("forcefield\n'{}'\n".format(forcefield))
        out.write("charge_assignment\n'{}'\n".format(charge_assignment))
        # Writing out individual atoms
        for i, atom in enumerate(molecule):
            out.write(outformat.format(unit=i+1, atom=atom))
            out.write("vibration\n")
            out.write("  {}\n".format(len(atom.bonds)))
            if atom.bonds:
                out.write("  {}\n".format(
                    ' '.join(str(ot.index + 1)
                             for ot in atom.bonded_atoms)
                    ))
            out.write("improper torsion\n")
            # Only "central" impropers count
            # Need to detect when an atom is in the middle
            out.write("  {}\n".format(0))


def write_coords(atomgroup):
    """Write a towhee_coords file"""
    with open('towhee_coords', 'w') as out:
        for atom in atomgroup:
            out.write("{pos[0]} {pos[1]} {pos[2]}\n".format(pos=atom.position))
