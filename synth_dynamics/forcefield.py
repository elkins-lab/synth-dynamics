import numpy as np
from scipy.spatial.distance import pdist, squareform


class ANMForceField:
    def __init__(
        self, equilibrium_coords: np.ndarray, cutoff: float = 15.0, spring_constant: float = 1.0
    ) -> None:
        """
        Anisotropic Network Model Force Field.

        Args:
            equilibrium_coords: (N, 3) array of C-alpha equilibrium positions.
            cutoff: Distance cutoff for interactions in Angstroms.
            spring_constant: Uniform spring constant k.
        """
        self.x0 = equilibrium_coords
        self.cutoff = cutoff
        self.k = spring_constant
        self.n_atoms = len(equilibrium_coords)

        # Precompute equilibrium distances and adjacency matrix
        dist_matrix = squareform(pdist(self.x0))
        self.adj = (dist_matrix < cutoff) & (dist_matrix > 0)
        self.r0 = dist_matrix

    def compute_forces(self, current_coords: np.ndarray) -> np.ndarray:
        """
        Computes the harmonic forces on each atom.

        Args:
            current_coords: (N, 3) array of current positions.
        Returns:
            forces: (N, 3) array of forces.
        """
        # Calculate current distances and difference vectors
        # diff[i, j] = r_i - r_j
        diff = current_coords[:, np.newaxis, :] - current_coords[np.newaxis, :, :]
        dist = np.linalg.norm(diff, axis=2)

        # Avoid division by zero
        dist_inv = np.zeros_like(dist)
        mask = dist > 0
        dist_inv[mask] = 1.0 / dist[mask]

        # Force magnitude matrix: F_ij = -k * (r_ij - r0_ij)
        # We only care about pairs in the adjacency matrix
        force_mag = -self.k * (dist - self.r0)

        # Full force vector matrix: F_vec_ij = F_ij * (diff_ij / dist_ij)
        # Shape: (N, N, 3)
        force_vecs = (force_mag * dist_inv)[:, :, np.newaxis] * diff

        # Zero out inactive interactions
        force_vecs[~self.adj] = 0.0

        # Total force on atom i is sum over j
        forces = np.sum(force_vecs, axis=1)

        return np.asarray(np.sum(force_vecs, axis=1))
