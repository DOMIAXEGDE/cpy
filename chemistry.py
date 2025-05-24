#!/usr/bin/env python3
"""
Generate a textual + visual library of molecules built from ALL 118 elements.

• Mode 1  – enumerate 1-N-atom combos and write  'Molecule k [valid|invalid]: <SMILES>'
• Mode 2  – render selected lines of that library as 300×300 PNGs
• Mode 3  – exit
• Quick   – 'python chem118.py all'  ==> writes the full library (N=3) then exits

Requires:  pip install rdkit pillow         (or  conda install -c conda-forge rdkit)
"""

from __future__ import annotations

import sys
from itertools import combinations_with_replacement
from pathlib import Path
from typing import List, Tuple

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.rdchem import Mol
from rdkit import RDLogger

RDLogger.DisableLog("rdApp.*")         # silence noisy valence warnings

# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------

# IUPAC 2023 list – symbols only
ELEMENTS: List[str] = [
    "H", "He",
    "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
    "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb",
    "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm",
    "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
    "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn",
    "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
]

ORGANIC = {"B", "C", "N", "O", "P", "S", "F", "Cl", "Br", "I"}   # won’t need [Brackets]

# --------------------------------------------------------------------------
# BASIC UTILITIES
# --------------------------------------------------------------------------

def prompt(msg: str, cast, cond=lambda x: True):
    """Simple validated input prompt."""
    while True:
        try:
            val = cast(input(msg))
            if cond(val):
                return val
        except Exception:
            pass
        print("  ✖ Invalid, please try again.")

def bracketed(sym: str) -> str:
    """Return SMILES atom token, bracketed if non-organic subset."""
    return sym if sym in ORGANIC else f"[{sym}]"

def build_smiles(combo: Tuple[str, ...]) -> str:
    """
    Convert a tuple of element symbols into a linear single-bond chain
    e.g. ('C','O','Cl')  ->  'C[O][Cl]'
    """
    return "".join(bracketed(e) for e in combo)

def mol_from_smiles(smi: str) -> Tuple[Mol | None, bool]:
    """Return Mol object and validity flag (False if RDKit sanitisation fails)."""
    mol = Chem.MolFromSmiles(smi, sanitize=False)
    if mol is None:
        return None, False
    try:
        Chem.SanitizeMol(mol)
        return mol, True
    except Exception:
        # keep un-sanitised Mol for depiction? RDKit draws even unsanitised
        return mol, False

# --------------------------------------------------------------------------
# MODE 1 – ENUMERATION
# --------------------------------------------------------------------------

def enumerate_library(max_atoms: int, out_file: Path):
    combos = []
    for length in range(1, max_atoms + 1):
        combos.extend(combinations_with_replacement(ELEMENTS, length))

    total = len(combos)
    print(f"▶ Generating {total:,} distinct combinations (1..{max_atoms} atoms) …")
    with out_file.open("w", encoding="utf-8") as f:
        for idx, combo in enumerate(combos):
            smi = build_smiles(combo)
            _, ok = mol_from_smiles(smi)
            flag = "valid" if ok else "invalid"
            f.write(f"Molecule {idx} {flag}: {smi}\n")
            if idx and idx % 50_000 == 0:
                print(f"  …{idx:,} done")

    print(f"✓ Finished.  Library saved to {out_file} ({total:,} lines).")

# --------------------------------------------------------------------------
# MODE 2 – VISUALISATION
# --------------------------------------------------------------------------

def render_pngs(lib_file: Path, selection: List[int]):
    with lib_file.open(encoding="utf-8") as f:
        lines = list(f)

    n = len(lines)
    for i in selection:
        if not (1 <= i <= n):
            print(f"  ✖ Line {i} outside 1..{n}, skipping.")
            continue
        tag, smi = lines[i - 1].split(":", 1)
        mol, ok = mol_from_smiles(smi.strip())
        if not ok or mol is None:
            print(f"  ⚠ Molecule {i} is invalid – no PNG generated.")
            continue
        img = Draw.MolToImage(mol, size=(300, 300))
        fname = f"molecule_{i}.png"
        img.save(fname)
        print(f"  ✓ Saved {fname}")

# --------------------------------------------------------------------------
# QUICK “ALL” ENTRY POINT
# --------------------------------------------------------------------------

if len(sys.argv) == 2 and sys.argv[1].lower() == "all":
    enumerate_library(max_atoms=3, out_file=Path("all118_library.txt"))
    sys.exit(0)

# --------------------------------------------------------------------------
# MAIN MENU
# --------------------------------------------------------------------------

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║            118-Element Molecule Generator            ║
╚══════════════════════════════════════════════════════╝
"""
print(BANNER)

while True:
    mode = prompt("Enter 1-generate  2-to-PNG  3-exit : ", int, lambda x: x in {1, 2, 3})
    if mode == 1:
        atoms = prompt("Max atoms per molecule (1-4 OK on a laptop) [default 3]: ",
                       int, lambda x: x >= 1)
        outfile = Path(prompt("Output file name [e.g. lib.txt]: ", str))
        enumerate_library(atoms, outfile)

    elif mode == 2:
        libfile = Path(prompt("Library file name: ", str))
        if not libfile.exists():
            print("  ✖ File not found.")
            continue
        span = prompt("Line numbers or ranges (e.g. 1-5,8,10-12): ", str)
        chosen: List[int] = []
        for part in span.split(","):
            if "-" in part:
                a, b = map(int, part.split("-"))
                chosen.extend(range(a, b + 1))
            else:
                chosen.append(int(part))
        render_pngs(libfile, chosen)

    else:
        print("Good-bye!")
        break
