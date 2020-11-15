"""Create a DL Monte config file from PDB"""

import MDAnalysis as mda


def getname(name):
    if name.startswith('Z'):
        return 'Zn'
    elif name.startswith('H'):
        return 'H'
    else:
        return name


def write_config(atomgroup):
    ts = atomgroup.universe.trajectory.ts

    with open('config.out', 'w') as output:
        output.write('An amazing config file\n')
        output.write(" 0 1\n")  # Only coordinates, Cartesian format
        for row in ts.triclinic_dimensions:  # box as 3 vectors
            output.write("{row[0]} {row[1]} {row[2]}\n".format(row=row))
            output.write("NUMMOL 1 1 1500\n")  # number of molecules and max of each

        output.write("MOLECULE IRMOF 3392 3392\n")
        for atom in atomgroup:
            output.write("{} core\n".format(atom.name))
            output.write(" {pos[0]} {pos[1]} {pos[2]}\n".format(pos=atom.position))


if __name__ == '__main__':
    u = mda.Universe('IRMOF.pdb')

    data = open('irmofcharges.out').readlines()
    names = [getname(line.split()[0]) for line in data]
    charges = [float(line.split()[-1]) for line in data]

    u.atoms.names = names
    u.atoms.charges = charges

    write_config(u.atoms)
