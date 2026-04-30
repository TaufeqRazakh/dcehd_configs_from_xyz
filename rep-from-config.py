#!/usr/bin/env python3
"""
Replicate a numeric CONFIG/XYZ-like file with scaled coordinates.

Example:
python3 rep-from-config.py eval-config/P25108_2_orthorhombic.xyz 2 2 2
"""

import argparse
from pathlib import Path


UNIT_CELL_VECTORS = (
    (7.27, 0.0, 0.0),
    (0.0, 7.27, 0.0),
    (0.0, 0.0, 14.105),
)


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


def replicate(atom_types, scaled_positions, nx, ny, nz):
    rep_atoms = []
    for ix in range(nx):
        for iy in range(ny):
            for iz in range(nz):
                for atom_type, (x, y, z) in zip(atom_types, scaled_positions):
                    rep_atoms.append(
                        (
                            atom_type,
                            (x + ix) / nx,
                            (y + iy) / ny,
                            (z + iz) / nz,
                        )
                    )
    return rep_atoms


def write_config(path, atoms):
    with path.open("w") as config:
        config.write(f"{len(atoms)}\n")
        for atom_type, x, y, z in atoms:
            config.write(f"{atom_type:>2s}  {x:12.8f} {y:12.8f} {z:12.8f}\n")


def replicated_cell(cell_vectors, nx, ny, nz):
    replicas = (nx, ny, nz)
    return tuple(
        tuple(component * replicas[row] for component in vector)
        for row, vector in enumerate(cell_vectors)
    )


def print_cell(title, cell_vectors):
    print(title)
    print("[")
    for vector in cell_vectors:
        print(f"  [{vector[0]:12.8f}, {vector[1]:12.8f}, {vector[2]:12.8f}]")
    print("]")


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
    args = parser.parse_args()

    atom_types, scaled_positions = read_config(args.input_file)
    replicated_atoms = replicate(atom_types, scaled_positions, args.nx, args.ny, args.nz)
    write_config(args.output_file, replicated_atoms)
    output_cell = replicated_cell(UNIT_CELL_VECTORS, args.nx, args.ny, args.nz)

    print(f"Input atoms: {len(atom_types)}")
    print(f"Replication: {args.nx} {args.ny} {args.nz}")
    print(f"Output atoms: {len(replicated_atoms)}")
    print_cell("Cell before replication:", UNIT_CELL_VECTORS)
    print_cell("Cell after replication:", output_cell)
    print(f"File opened: {args.output_file}")


if __name__ == "__main__":
    main()
