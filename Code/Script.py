#!/usr/bin/env python3

# 1. Load Libraries

from collections import defaultdict
import math

# 2. Load PDB File

class Atom:
    def __init__(self, name, residue, chain, res_id, x, y, z, element):
        self.name = name
        self.residue = residue
        self.chain = chain
        self.res_id = res_id
        self.coord = (x, y, z)
        self.element = element

    def distance(self, other):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.coord, other.coord)))


def load_pdb(filepath):
    atoms = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                name = line[12:16].strip()
                residue = line[17:20].strip()
                chain = line[21].strip()
                res_id = int(line[22:26])
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                element = line[76:78].strip()

                atoms.append(Atom(name, residue, chain, res_id, x, y, z, element))
    return atoms

# 3. Structure Classes

class HydrogenBond:
    def __init__(self, donor, acceptor, distance):
        self.donor = donor
        self.acceptor = acceptor
        self.distance = distance

    def is_valid(self, cutoff=3.5):
        return self.distance <= cutoff


class BasePair:
    def __init__(self, res1_id, res2_id, res1_name, res2_name):
        self.res1_id = res1_id
        self.res2_id = res2_id
        self.res1_name = res1_name
        self.res2_name = res2_name

    def __repr__(self):
        return f"{self.res1_name}{self.res1_id}-{self.res2_name}{self.res2_id}"


class TertiaryCoordinates:
    def __init__(self):
        self.residues = defaultdict(list)

    def add_atom(self, atom):
        key = (atom.chain, atom.res_id, atom.residue)
        self.residues[key].append(atom)

    def get_residue_atoms(self, key):
        return self.residues[key]

# 4. Detect Hydrogen Bonds

def detect_hydrogen_bonds(atoms):
    hbonds = []
    for i, atom1 in enumerate(atoms):
        if atom1.element not in ['N', 'O']:
            continue
        for atom2 in atoms[i+1:]:
            if atom2.element not in ['N', 'O']:
                continue

            dist = atom1.distance(atom2)
            hbond = HydrogenBond(atom1, atom2, dist)

            if hbond.is_valid():
                hbonds.append(hbond)

    return hbonds

# 5. Infer Base Pairs (Simplified)

def infer_base_pairs(hbonds):
    pair_counts = defaultdict(int)

    for hb in hbonds:
        res1 = (hb.donor.chain, hb.donor.res_id, hb.donor.residue)
        res2 = (hb.acceptor.chain, hb.acceptor.res_id, hb.acceptor.residue)

        if res1 != res2:
            pair_counts[(res1, res2)] += 1
            pair_counts[(res2, res1)] += 1

    base_pairs = []
    visited = set()

    for (res1, res2), count in pair_counts.items():
        if count >= 2 and (res2, res1) not in visited:
            base_pairs.append(
                BasePair(res1[1], res2[1], res1[2], res2[2])
            )
            visited.add((res1, res2))

    return base_pairs

# 6. Bracket Notation

def generate_bracket_notation(base_pairs, residues):
    """
    residues: sorted list of residue IDs
    """
    pairing_map = {}

    for bp in base_pairs:
        pairing_map[bp.res1_id] = bp.res2_id
        pairing_map[bp.res2_id] = bp.res1_id

    notation = ['.'] * len(residues)
    index_map = {res_id: i for i, res_id in enumerate(residues)}

    for res1, res2 in pairing_map.items():
        if res1 < res2:
            notation[index_map[res1]] = '('
            notation[index_map[res2]] = ')'

    return ''.join(notation)

# 7. Main Pipeline

def main(pdb_file):
    atoms = load_pdb(pdb_file)

    structure = TertiaryCoordinates()
    for atom in atoms:
        structure.add_atom(atom)

    hbonds = detect_hydrogen_bonds(atoms)
    base_pairs = infer_base_pairs(hbonds)

    # Get sorted residues
    residues = sorted(set(atom.res_id for atom in atoms))

    notation = generate_bracket_notation(base_pairs, residues)

    print("Detected Base Pairs:")
    for bp in base_pairs:
        print(bp)

    print("\nBracket Notation:")
    print(notation)
    
    with open("output.txt", "w") as f:
        f.write("Detected Base Pairs:\n")
        for bp in base_pairs:
            f.write(f"{bp}\n")
        f.write("\n")
        f.write("\nBracket Notation:\n")
        f.write(notation)

# Run the script

if __name__ == "__main__":
    pdb_path = "/adhome/a/au/aurelio.vitale/Projet_GPI_AV/7kef.pdb"  # Replace with your file
    main(pdb_path)