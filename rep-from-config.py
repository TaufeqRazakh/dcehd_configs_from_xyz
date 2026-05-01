#!/usr/bin/env python3
"""
Replicate a numeric CONFIG/XYZ-like file with scaled coordinates using ASE.

Example:
.venv/bin/python rep-from-config.py eval-config/P25108_2_orthorhombic.xyz 2 2 2
"""

import argparse
from pathlib import Path

import numpy as np
import ase.io
import ase.build
from ase import Atoms


UNIT_CELL_VECTORS = (
    (7.27, 0.0, 0.0),
    (0.0, 7.27, 0.0),
    (0.0, 0.0, 14.105),
)

TYPE_TO_SYMBOL = {
    "1": "Si",
    "2": "C",
    "3": "H",
}
SYMBOL_TO_TYPE = {symbol: atom_type for atom_type, symbol in TYPE_TO_SYMBOL.items()}


def read_config(path):
    lines = path.read_text().splitlines()
    if not lines:
        raise ValueError(f"{path} is empty")

    try:
        natoms = int(lines[0].split()[0])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"first line of {path} must contain the atom count") from exc

    remaining = lines[1:]
    if len(remaining) == natoms:
        data_lines = remaining
    else:
        data_lines = remaining[1:]

    data_lines = [line for line in data_lines if line.strip()]
    if len(data_lines) < natoms:
        raise ValueError(f"{path} says it has {natoms} atoms, but only {len(data_lines)} atom lines were found")

    atom_types = []
    scaled_positions = []
    for line_number, line in enumerate(data_lines[:natoms], start=2):
        fields = line.split()
        if len(fields) < 4:
            raise ValueError(f"line {line_number} must contain: type x y z")

        atom_types.append(fields[0])
        try:
            scaled_positions.append(tuple(float(value) for value in fields[1:4]))
        except ValueError as exc:
            raise ValueError(f"line {line_number} has a non-numeric coordinate") from exc

    return atom_types, scaled_positions


def build_atoms(atom_types, scaled_positions):
    try:
        symbols = [TYPE_TO_SYMBOL[atom_type] for atom_type in atom_types]
    except KeyError as exc:
        known_types = ", ".join(sorted(TYPE_TO_SYMBOL))
        raise ValueError(f"unknown atom type {exc.args[0]!r}; known types are: {known_types}") from exc

    return Atoms(
        symbols=symbols,
        scaled_positions=scaled_positions,
        cell=UNIT_CELL_VECTORS,
        pbc=True,
    )


def write_config(path, atoms):
    scaled_positions = atoms.get_scaled_positions(wrap=True)
    symbols = atoms.get_chemical_symbols()

    with path.open("w") as config:
        config.write(f"{len(atoms)}\n")
        for symbol, (x, y, z) in zip(symbols, scaled_positions):
            atom_type = SYMBOL_TO_TYPE[symbol]
            config.write(f"{atom_type:>2s}  {x:12.8f} {y:12.8f} {z:12.8f}\n")


def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("replication values must be positive integers")
    return parsed


def main():
    parser = argparse.ArgumentParser(
        prog="rep-from-config.py",
        description="Replicate a CONFIG/XYZ-like file containing type and scaled x y z coordinates.",
    )
    parser.add_argument("input_file", type=Path, help="CONFIG/XYZ-like file to replicate")
    parser.add_argument("nx", type=positive_int, help="number of replicas in x")
    parser.add_argument("ny", type=positive_int, help="number of replicas in y")
    parser.add_argument("nz", type=positive_int, help="number of replicas in z")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=Path("IN.CONFIG_SCALED"),
        help="output filename (default: IN.CONFIG_SCALED)",
    )
    parser.add_argument(
        "--xyz_file",
        type=Path,
        default=Path("out.xyz"),
        help="replicated XYZ output filename (default: out.xyz)",
    )
    args = parser.parse_args()

    atom_types, scaled_positions = read_config(args.input_file)
    atoms = build_atoms(atom_types, scaled_positions)
    transformation = np.diag([args.nx, args.ny, args.nz])
    replicated_atoms = ase.build.make_supercell(atoms, transformation)

    write_config(args.output_file, replicated_atoms)
    ase.io.write(args.xyz_file, replicated_atoms)

    print(f"Input atoms: {len(atom_types)}")
    print(f"Replication: {args.nx} {args.ny} {args.nz}")
    print(f"Output atoms: {len(replicated_atoms)}")
    print("MD CELL before replication ")
    print(atoms.get_cell().array)
    print("MD CELL after replication ")
    print(replicated_atoms.get_cell().array)
    print(f"File opened: {args.output_file}")
    print(f"XYZ file opened: {args.xyz_file}")


if __name__ == "__main__":
    main()
