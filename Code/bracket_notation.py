#!/usr/bin/env python3

# 1. Load Libraries

from collections import defaultdict
import math
import os
import sys

# 2. Creation of the different Classes

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

# 3. Structurale Information into OOP (object-oriented programming) -> Load PDB file & Extract all the data & process it for bracket notation
# 3.1 Load PDB File & Extract Atoms

def load_pdb(filepath):
    atoms = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("ATOM"):

                name = line[12:16].strip() # strip remove all the spaces
                residue = line[17:20].strip()
                chain = line[21].strip()
                res_id = int(line[22:26])

                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                element = line[76:78].strip()

                atoms.append(
                    Atom(name, residue, chain, res_id,
                         x, y, z, element)
                )

    return atoms

# 3.2 Detect Hydrogen Bonds

def detect_hydrogen_bonds(atoms):

    BACKBONE_ATOMS = {"O5'", "O3'", "O4'", "O2'","OP1", "OP2", "P"}

    VALID_ATOM_PAIRS = {

        ("A", "U"): {("N6", "O4"),("N1", "N3")},

        ("U", "A"): {("O4", "N6"),("N3", "N1")},

        ("G", "C"): {("O6", "N4"),("N1", "N3"),("N2", "O2")},

        ("C", "G"): {("N4", "O6"),("N3", "N1"),("O2", "N2")},

        ("G", "U"): {("O6", "N3"),("N1", "O2")},

        ("U", "G"): {("N3", "O6"),("O2", "N1")}
        
    }

    hbonds = []

    seen_atom_pairs = set()

    for i, atom1 in enumerate(atoms):

        # uniquement N/O
        if atom1.element not in ['N', 'O']:
            continue

        # exclure backbone
        if atom1.name in BACKBONE_ATOMS:
            continue

        for atom2 in atoms[i + 1:]:

            if atom2.element not in ['N', 'O']:
                continue

            if atom2.name in BACKBONE_ATOMS:
                continue

            # même résidu
            if (
                atom1.chain == atom2.chain
                and
                atom1.res_id == atom2.res_id
            ):
                continue

            # éviter résidus proches
            if abs(atom1.res_id - atom2.res_id) <= 3:
                continue

            pair_type = (
                atom1.residue,
                atom2.residue
            )

            # seulement AU / CG / GU
            if pair_type not in VALID_ATOM_PAIRS:
                continue

            # vérifier vrais atomes Watson-Crick
            if (
                atom1.name,
                atom2.name
            ) not in VALID_ATOM_PAIRS[pair_type]:
                continue

            # éviter doublons
            atom_pair = tuple(sorted([
                (atom1.res_id, atom1.name),
                (atom2.res_id, atom2.name)
            ]))

            if atom_pair in seen_atom_pairs:
                continue

            seen_atom_pairs.add(atom_pair)

            dist = atom1.distance(atom2)

            hbond = HydrogenBond(
                atom1,
                atom2,
                dist
            )

            # cutoff imposé
            if hbond.is_valid(cutoff=3.0):

                hbonds.append(hbond)

    return hbonds

# 3.3 Infer Base Pairs

def infer_base_pairs(hbonds):

    EXPECTED_HBONDS = {
        ("C", "G"): 3,
        ("G", "C"): 3,
        ("A", "U"): 2,
        ("U", "A"): 2,
        ("G", "U"): 2,
        ("U", "G"): 2
    }

    pair_counts = defaultdict(int)

    for hb in hbonds:

        res1 = (
            hb.donor.chain,
            hb.donor.res_id,
            hb.donor.residue
        )

        res2 = (
            hb.acceptor.chain,
            hb.acceptor.res_id,
            hb.acceptor.residue
        )

        if res1 == res2:
            continue

        # évite voisins proches
        if abs(res1[1] - res2[1]) <= 3:
            continue

        pair_type = (res1[2], res2[2])

        # seulement AU / CG / GU
        if pair_type not in EXPECTED_HBONDS:
            continue

        pair = tuple(sorted([res1, res2]))

        pair_counts[pair] += 1

    base_pairs = []

    used = set()

    for (res1, res2), count in sorted(
        pair_counts.items(),
        key=lambda x: -x[1]
    ):

        pair_type = (res1[2], res2[2])

        required = EXPECTED_HBONDS[pair_type]

        # nombre minimal de H-bonds
        if count < required:
            continue

        # un seul partenaire
        if res1 in used or res2 in used:
            continue

        base_pairs.append(
            BasePair(
                res1[1],
                res2[1],
                res1[2],
                res2[2]
            )
        )

        used.add(res1)
        used.add(res2)

    return base_pairs

# 3.4 Extract the sequence

def extract_sequence(atoms):

    residue_map = {}

    for atom in atoms:

        if atom.res_id not in residue_map:
            residue_map[atom.res_id] = atom.residue

    # ordre des résidus
    sorted_res = sorted(residue_map.items())

    # conversion en séquence
    sequence = ''.join(res for _, res in sorted_res)

    return sequence

# 4. Bracket Notation

def generate_bracket_notation(base_pairs, residues):

    pairing_map = {}

    for bp in base_pairs:
        pairing_map[bp.res1_id] = bp.res2_id
        pairing_map[bp.res2_id] = bp.res1_id

    notation = ['.'] * len(residues)

    index_map = {
        res_id: i
        for i, res_id in enumerate(residues)
    }

    for res1, res2 in pairing_map.items():

        if res1 < res2:
            notation[index_map[res1]] = '('
            notation[index_map[res2]] = ')'

    return ''.join(notation)

# 5. Main Pipeline

def process_pdb(pdb_file):

    atoms = load_pdb(pdb_file)

    structure = TertiaryCoordinates()
    for atom in atoms:
        structure.add_atom(atom)

    hbonds = detect_hydrogen_bonds(atoms)
    base_pairs = infer_base_pairs(hbonds)

    residues = sorted(set(atom.res_id for atom in atoms))

    sequence = extract_sequence(atoms)

    notation = generate_bracket_notation(base_pairs, residues)

    pdb_name = os.path.splitext(os.path.basename(pdb_file))[0]
    output_dir = "Output_PDB_BracketNotation"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        f"{pdb_name}_bracketnotation.txt"
    )

    print("RNA Sequence:\n")
    print(sequence + "\n\n")
    
    print("Bracket Notation:\n")
    print(notation + "\n")
    
    with open(output_file, "w") as f:
        f.write("RNA Sequence:\n")
        f.write(sequence + "\n\n")
        f.write("Bracket Notation:\n")
        f.write(notation + "\n")
        
    print(f"Bracket notation saved to: {output_file}")

    return notation, output_file

# 6. Run the Script

if __name__ == "__main__":

    # Check argument
    if len(sys.argv) != 2:
        print("Usage:")
        print(" -> " + sys.argv[0] + "your_pdb_file.pdb")
        sys.exit(1)

    pdb_path = sys.argv[1]

    # Verify extension
    if not pdb_path.endswith(".pdb"):
        print("Error: input file must be a .pdb file")
        sys.exit(1)

    process_pdb(pdb_path)
