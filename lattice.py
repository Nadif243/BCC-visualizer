# lattice.py
import numpy as np

# --- BCC Atom Positions ---
bcc_atom1 = np.array([
    [-1, -3, 1], [1, -3, 1], [1, -1, 1], [-1, -1, 1],
    [-1, -3, 3], [1, -3, 3], [1, -1, 3], [-1, -1, 3]
], dtype=float)

bcc_atom2 = np.array([
    [1, -3, -1], [3, -3, -1], [3, -1, -1], [1, -1, -1],
    [1, -3,  1], [3, -3,  1], [3, -1,  1], [1, -1,  1]
], dtype=float)

bcc_atom3 = np.array([
    [1,  1, 1], [3,  1, 1], [3, -1, 1], [1, -1, 1],
    [1,  1, 3], [3,  1, 3], [3, -1, 3], [1, -1, 3]
], dtype=float)

# --- Derived Data ---
CUBES = [bcc_atom1, bcc_atom2, bcc_atom3]

POINTS = np.array([coord for cube in CUBES for coord in cube], dtype=float)

CUBE_CENTERS = np.array([cube.mean(axis=0) for cube in CUBES], dtype=float)

INTERSECTION = np.array([1, -1, 1], dtype=float)

# --- Edge Connectivity (indices within a single cube) ---
CUBE_EDGES = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # bottom face
    [4, 5], [5, 6], [6, 7], [7, 4],  # top face
    [0, 4], [1, 5], [2, 6], [3, 7]   # vertical edges
]
