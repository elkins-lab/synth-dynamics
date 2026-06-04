import MDAnalysis as mda  # noqa: N813
import numpy as np


class System:
    def __init__(self, pdb_path: str):
        """
        Initializes the system by loading a PDB file and extracting C-alpha atoms.

        Args:
            pdb_path: Path to the input PDB file.
        """
        import os

        if not os.path.exists(pdb_path):
            raise FileNotFoundError(f"PDB file not found: {pdb_path}")

        self.universe = mda.Universe(pdb_path)
        self.ca_atoms = self.universe.select_atoms("name CA")

        if len(self.ca_atoms) == 0:
            raise ValueError(f"No C-alpha atoms found in {pdb_path}")

        # Store equilibrium coordinates (reference state)
        self.equilibrium_coords = self.ca_atoms.positions.copy()
        self.n_atoms = len(self.ca_atoms)

    @property
    def positions(self) -> np.ndarray:
        return np.asarray(self.ca_atoms.positions)

    @positions.setter
    def positions(self, new_positions: np.ndarray) -> None:
        if not isinstance(new_positions, np.ndarray):
            new_positions = np.asarray(new_positions)

        if new_positions.shape != (self.n_atoms, 3):
            raise ValueError(
                f"Invalid positions shape: expected ({self.n_atoms}, 3), got {new_positions.shape}"
            )

        self.ca_atoms.positions = new_positions
