import MDAnalysis as mda
import numpy as np

class System:
    def __init__(self, pdb_path: str):
        """
        Initializes the system by loading a PDB file and extracting C-alpha atoms.
        
        Args:
            pdb_path: Path to the input PDB file.
        """
        self.universe = mda.Universe(pdb_path)
        self.ca_atoms = self.universe.select_atoms("name CA")
        
        if len(self.ca_atoms) == 0:
            raise ValueError(f"No C-alpha atoms found in {pdb_path}")
            
        # Store equilibrium coordinates (reference state)
        self.equilibrium_coords = self.ca_atoms.positions.copy()
        self.n_atoms = len(self.ca_atoms)
        
    @property
    def positions(self):
        return self.ca_atoms.positions

    @positions.setter
    def positions(self, new_positions):
        self.ca_atoms.positions = new_positions
