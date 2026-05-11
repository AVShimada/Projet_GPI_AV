# Projet_GPI_AV

## Master GPI project

**3D and 2D RNA structure / Structurale bioimagerie**

![RNA](https://www.yourgenome.org/wp-content/uploads/2023/11/1590-shutterstock_2362113623-1920x1047.jpg)

- This project is a student project for BioInformatic and Structurale BioImagerie Master 1, there are 2 possible subject to choose from : 
- **3D and 2D RNA structure** -> Identify 2D structure of RNA based on it's 3D structure (from a PDB file) 
- **Structurale bioimagerie** -> Micrograph particle extraction

- This project is done in python and could ask to download libraries if needed.

---
Track list of the project advancement :
- [x] Create the repertisory
- [x] Choose between the subject
- [x] Create a plan for the coding
- [x] Create the script
- [x] Output file directly named by the pdb name (might want to also add it as a header in the file not sure)
- [ ] Create an interface to drop the pdb file directly (launch a .exe rather than lauching code)
- [ ] Display directly the bracket inside the .exe ?
- [ ] Visualize how the pair base are link with an option ?

---
Plan for the project:
1. Load Librairie
2. Load PDB file
3. Encoder l'information structurale en POO
4. The way we are going to do it : Classe Atom - Class HydrogenBond - Classe BasePair - Classe TertiaryCoordinates
5. Describe pair base in the bracket notation form -> () means the nucleotide is paired and the sens of the parenthesis help us to say with which nucleotide it's paired . means no link with other nucleotide

---
Commande to download pdb file directly:
curl -O https://files.rcsb/org/view/fichier.pdb

---
Row TER of pdbfile -> end of the chain
We only get the bracket for 1 chain seens they are the same.