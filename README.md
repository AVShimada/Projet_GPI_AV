# Projet_GPI_AV

## Master GPI project

**3D and 2D RNA structure / Structurale bioimagerie**

![RNA](https://www.yourgenome.org/wp-content/uploads/2023/11/1590-shutterstock_2362113623-1920x1047.jpg)

- This project is a student project for BioInformatic and Structurale BioImagerie Master 1, there are 2 possible subject to choose from : 
- **3D and 2D RNA structure** -> Identify 2D structure of RNA based on it's 3D structure (from a PDB file) 
- **Structurale bioimagerie** -> Micrograph particle extraction

[!NOTE] 
This project is done in python and could ask to download libraries if needed.

[!TIP] 
All the ways to get the bracket notation from your RNA pdb file:

1. Terminal : 
- Python Script : Activate script -> chmod +x bracket_notation.py / Run the script -> ./bracket_notation.py FILE.pdb
- Executable : bracket_notation / bracket_notation.exe (Linux/Windows) Run the script -> ./bracket_notation FILE.pdb / ./bracket_notation.exe FILE.pdb
2. User GUI :
- bracket_notation_gui / bracket_notation_gui.exe (Linux/Windows) -> Launch your executable -> Drag and drop your PDB file directly inside the application

[!IMPORTANT] 
Download the zip file specific for your OS

---
Track list of the project advancement :
- [x] Create the repertisory
- [x] Choose between the subject
- [x] Create a plan for the coding
- [x] Create the script
- [x] Output file directly named by the pdb name (might want to also add it as a header in the file not sure)
- [x] Make a terminal only : bracket_notation.exe fichier.pdb -> fichier_bracketnotation.txt (Right now need to put the complete PATH)
- [x] Create an interface to drop the pdb file directly (launch a .exe rather than lauching code)
- [x] Display directly the bracket inside the .exe ?
- [x] File output -> Directly inside a specialized directory
- [ ] Annotation of the code
- [ ] Version that use package to limit of line in the main script
- [ ] Relaunch concatenate on windows to get a .exe right now its only an executable for Linux or terminal python one
- [ ] Get the first line of the PDB file to get the title -> What is this protein to at least show it in terminal
- [ ] Modif UI (police of writing, etc)
- [ ] Modif github repository -> Script Python + Exec linux/windows / Executable GUI linux/windows / Output PDB 
- [ ] Zip for Linux and Windows Seperate
- [ ] Verify which library need to be installed -> tell the user to install them : show a command to directly install them all
- [ ] Visualize how the pair base are link with an option ?

---
Plan for the project:
1. Load Librairie
2. Load PDB file
3. Structurale information into Oriented Object Programmation (OOP)
4. The way we are going to do it : Classe Atom - Class HydrogenBond - Classe BasePair - Classe TertiaryCoordinates
5. Describe pair base in the bracket notation form -> () means the nucleotide is paired and the sens of the parenthesis help us to say with which nucleotide it's paired . means no link with other nucleotide

---
**Command to download pdb file directly:**
curl -O https://files.rcsb/org/view/fichier.pdb

---
**Command to concatenate the script.py into a .exe:**
pyinstaller --onefile bracket_notation.py

---
**Activate the script:**
chmod +x bracket_notation.py

**Launch Script:**
./bracket_notation.py FILE.pdb

---
Information Random:

Row TER of pdbfile -> end of the chain

We only get the bracket for 1 chain seens they are the same.

Launch env to concatenate and all ... : source ~/venv/bin/activate

COLUMNS        DATA  TYPE    FIELD        DEFINITION
-------------------------------------------------------------------------------------
1 -  6         Record name   "ATOM  "
7 - 11        Integer       serial       Atom  serial number.
13 - 16        Atom          name         Atom name.
17             Character     altLoc       Alternate location indicator.
18 - 20        Residue name  resName      Residue name.
22             Character     chainID      Chain identifier.
23 - 26        Integer       resSeq       Residue sequence number.
27             AChar         iCode        Code for insertion of residues.
31 - 38        Real(8.3)     x            Orthogonal coordinates for X in Angstroms.
39 - 46        Real(8.3)     y            Orthogonal coordinates for Y in Angstroms.
47 - 54        Real(8.3)     z            Orthogonal coordinates for Z in Angstroms.
55 - 60        Real(6.2)     occupancy    Occupancy.
61 - 66        Real(6.2)     tempFactor   Temperature  factor.
77 - 78        LString(2)    element      Element symbol, right-justified.
79 - 80        LString(2)    charge       Charge  on the atom.