import MDAnalysis as mda
from .system import System
from .forcefield import ANMForceField
from .integrator import LangevinIntegrator

class Simulation:
    def __init__(self, system, forcefield, integrator):
        """
        Orchestrates the Langevin dynamics simulation.
        
        Args:
            system: System instance.
            forcefield: ForceField instance.
            integrator: Integrator instance.
        """
        self.system = system
        self.ff = forcefield
        self.integrator = integrator
        
    def run(self, n_steps, output_path, stride=10):
        """
        Runs the simulation and saves the trajectory.
        
        Args:
            n_steps: Total number of integration steps.
            output_path: Path to save the trajectory (e.g., .dcd or .pdb).
            stride: Frequency of saving frames.
        """
        writer = mda.Writer(output_path, self.system.n_atoms)
        
        for i in range(n_steps):
            forces = self.ff.compute_forces(self.system.positions)
            new_positions = self.integrator.step(self.system.positions, forces)
            self.system.positions = new_positions
            
            if i % stride == 0:
                writer.write(self.system.ca_atoms)
                
        writer.close()
        print(f"Simulation complete. Trajectory saved to {output_path}")
