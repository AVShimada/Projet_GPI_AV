# Projet_GPI_AV

## Master GPI project

**3D and 2D RNA structure / Structurale bioimagerie**

![RNA](https://www.yourgenome.org/wp-content/uploads/2023/11/1590-shutterstock_2362113623-1920x1047.jpg)

1. This project is a student project for BioInformatic and Structurale BioImagerie Master 1, there are 2 possible subject to choose from : 
    - **3D and 2D RNA structure** -> Identify 2D structure of RNA based on it's 3D structure (from a PDB file) 
    - **Structurale bioimagerie** -> Micrograph particle extraction : https://github.com/inzhirmelsh/GPI

>[!NOTE] 
>This project is done in python and could ask to download libraries if needed.

>[!IMPORTANT] 
>Download the zip file specific for your OS
>`bracket_notation_linux` or `bracket_notation_windows`

>[!TIP]
>All the ways to get the bracket notation from your RNA PDB file:
>
>1. **Terminal**
>   - **Python script**  
>     Activate the script:
>     ```bash
>     chmod +x bracket_notation.py
>     ```
>     Run it:
>     ```bash
>     ./bracket_notation.py FILE.pdb
>     ```
>
>   - **Executable** (`Linux` / `Windows`)  
>     Run:
>     ```bash
>     ./bracket_notation FILE.pdb
>     ```
>     or
>     ```bash
>     ./bracket_notation.exe FILE.pdb
>     ```
>
>2. **GUI application**
>   - `bracket_notation_gui` or `bracket_notation_gui.exe` (`Linux` / `Windows`)
>   - Launch the application and drag & drop your PDB file directly into the window.

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
- [x] Relaunch concatenate on windows to get a .exe right now its only an executable for Linux or terminal python one
- [x] Modif github repository -> Script Python + Exec linux/windows / Executable GUI linux/windows / Output PDB 
- [x] Zip for Linux and Windows Seperate
- [x] RESULTAT DOIT AVOIR SEQUENCE ARN + BRACKET PAS JUSTE BRACKET /!\
- [ ] Add bpseq format : https://zeus.few.vu.nl/programs/k2nwww/static/data_formats.html
- [ ] Annotation of the code
- [ ] Version that use package to limit of line in the main script
- [ ] Get the first line of the PDB file to get the title -> What is this protein to at least show it in terminal
- [ ] Modif UI (police of writing, etc)
- [ ] Verify which library need to be installed -> tell the user to install them : show a command to directly install them all
- [ ] Visualize how the pair base are link with an option ?
- [ ] Why Cmd open behind the application on Windows ? (FIX if needed)

---
Plan for the project:
1. Load Librairie
2. Load PDB file
3. Structurale information into Oriented Object Programmation (OOP)
4. The way we are going to do it : Classe Atom - Class HydrogenBond - Classe BasePair - Classe TertiaryCoordinates
5. Describe pair base in the bracket notation form -> () means the nucleotide is paired and the sens of the parenthesis help us to say with which nucleotide it's paired . means no link with other nucleotide
6. BasePair can only be between AU, GC and GU in RNA and the bond is ~3 ANGSTRÖM
7. Put . for every nucleotide then replace . with () for basepairs detected

---
**Command to download pdb file directly:**
curl -O https://files.rcsb/org/view/fichier.pdb

---
**Command to concatenate the script.py into a .exe:**
Linux:
pyinstaller --onefile bracket_notation.py

Windows:
py -m PyInstaller --onefile bracket_notation.py
---
**Activate the script:**
chmod +x bracket_notation.py

**Launch Script:**
./bracket_notation.py FILE.pdb

**Launch env to concatenate python into executable**
source ~/venv/bin/activate

**Link site for github readme format :**
https://docs.github.com/fr/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

---
**PDB FILE FORMAT:**

| COLUMNS   | DATA TYPE     | FIELD      | DEFINITION |
|-----------|---------------|------------|------------|
| 1 - 6     | Record name   | "ATOM  "   | Record name |
| 7 - 11    | Integer       | serial     | Atom serial number |
| 13 - 16   | Atom          | name       | Atom name |
| 17        | Character     | altLoc     | Alternate location indicator |
| 18 - 20   | Residue name  | resName    | Residue name |
| 22        | Character     | chainID    | Chain identifier |
| 23 - 26   | Integer       | resSeq     | Residue sequence number |
| 27        | AChar         | iCode      | Code for insertion of residues |
| 31 - 38   | Real(8.3)     | x          | Orthogonal coordinates for X in Angstroms |
| 39 - 46   | Real(8.3)     | y          | Orthogonal coordinates for Y in Angstroms |
| 47 - 54   | Real(8.3)     | z          | Orthogonal coordinates for Z in Angstroms |
| 55 - 60   | Real(6.2)     | occupancy  | Occupancy |
| 61 - 66   | Real(6.2)     | tempFactor | Temperature factor |
| 77 - 78   | LString(2)    | element    | Element symbol, right-justified |
| 79 - 80   | LString(2)    | charge     | Charge on the atom |

---
**Expected Structure for 8D28.pdb:**

Sequence:

GGCGAUACCAGCCGAAAGGCCCUUGGCAGCGCC

Dot Bracket Notation:

((((...((.(((....)))....))...))))
