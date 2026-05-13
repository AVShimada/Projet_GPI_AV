#!/usr/bin/env python3

from collections import defaultdict
import math
import os
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD


# =====================================================
# 1. LOAD PDB
# =====================================================

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

                atoms.append(
                    Atom(name, residue, chain, res_id, x, y, z, element)
                )

    return atoms


# =====================================================
# 2. STRUCTURES
# =====================================================

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


class TertiaryCoordinates:
    def __init__(self):
        self.residues = defaultdict(list)

    def add_atom(self, atom):
        key = (atom.chain, atom.res_id, atom.residue)
        self.residues[key].append(atom)


# =====================================================
# 3. H-BONDS
# =====================================================

def detect_hydrogen_bonds(atoms):
    hbonds = []

    for i, atom1 in enumerate(atoms):
        if atom1.element not in ['N', 'O']:
            continue

        for atom2 in atoms[i + 1:]:
            if atom2.element not in ['N', 'O']:
                continue

            dist = atom1.distance(atom2)
            hbond = HydrogenBond(atom1, atom2, dist)

            if hbond.is_valid():
                hbonds.append(hbond)

    return hbonds


# =====================================================
# 4. BASE PAIRS
# =====================================================

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


# =====================================================
# 5. BRACKET NOTATION
# =====================================================

def generate_bracket_notation(base_pairs, residues):

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


# =====================================================
# 6. PIPELINE
# =====================================================

def process_pdb(pdb_file):

    atoms = load_pdb(pdb_file)

    structure = TertiaryCoordinates()
    for atom in atoms:
        structure.add_atom(atom)

    hbonds = detect_hydrogen_bonds(atoms)
    base_pairs = infer_base_pairs(hbonds)

    residues = sorted(set(atom.res_id for atom in atoms))

    notation = generate_bracket_notation(base_pairs, residues)

    pdb_name = os.path.splitext(os.path.basename(pdb_file))[0]
    output_dir = "Output_PDB_BracketNotation"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        f"{pdb_name}_bracketnotation.txt"
    )

    with open(output_file, "w") as f:
        f.write("Bracket Notation:\n")
        f.write(notation + "\n")

    return notation, output_file


# =====================================================
# 7. GUI
# =====================================================

def drop(event):

    file_path = event.data.strip("{}")

    if not file_path.endswith(".pdb"):
        messagebox.showerror("Error", "Please drop a .pdb file")
        return

    label.config(text="Processing...")

    result_label.config(state="normal")
    result_label.delete("1.0", "end")
    result_label.insert("end", "Running analysis...\n")
    result_label.config(state="disabled")

    root.update()

    try:
        notation, output_file = process_pdb(file_path)

        label.config(text="Drop another PDB file")

        result_label.config(state="normal")
        result_label.delete("1.0", "end")

        result_label.insert(
            "end",
            f"SUCCESS\n\n"
            f"Saved file:\n{output_file}\n\n"
            f"Length: {len(notation)}\n\n"
            f"Bracket Notation:\n\n{notation}\n"
        )

        result_label.config(state="disabled")

    except Exception as e:
        label.config(text="Drop a PDB file")
        messagebox.showerror("Error", str(e))


# =====================================================
# 8. WINDOW
# =====================================================

root = TkinterDnD.Tk()
root.title("PDB Bracket Notation")
root.geometry("850x650")

label = tk.Label(
    root,
    text="Drag & Drop a PDB file here",
    font=("Arial", 16),
    width=35,
    height=4,
    relief="ridge",
    bd=3
)
label.pack(pady=15)

label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', drop)


# Scrollable output area
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

result_label = tk.Text(
    frame,
    font=("Courier", 11),
    wrap="word",
    yscrollcommand=scrollbar.set
)

result_label.pack(fill="both", expand=True)
scrollbar.config(command=result_label.yview)

result_label.insert("end", "Waiting for PDB file...\n")
result_label.config(state="disabled")


root.mainloop()