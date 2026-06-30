"""
Orchestrates the Langevin dynamics simulation using the force field and integrator.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import MDAnalysis as mda  # noqa: N813

if TYPE_CHECKING:
    from synth_dynamics.forcefield import ANMForceField
    from synth_dynamics.integrator import LangevinIntegrator
    from synth_dynamics.system import System


class Simulation:
    """
    Manages the overall simulation loop, coordinating forces, integration steps, and trajectory I/O.
    """

    def __init__(
        self,
        system: System,
        forcefield: ANMForceField,
        integrator: LangevinIntegrator,
    ) -> None:
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

    def run(self, n_steps: int, output_path: str, stride: int = 10) -> None:
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
