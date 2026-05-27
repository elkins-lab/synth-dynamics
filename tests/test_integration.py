import os

import MDAnalysis as mda
import numpy as np

from synth_dynamics import ANMForceField, LangevinIntegrator, Simulation, System


def create_dummy_pdb(path):
    # Create a simple line of 5 CA atoms
    n_atoms = 5
    coords = np.zeros((n_atoms, 3))
    coords[:, 0] = np.arange(n_atoms) * 3.8  # 3.8 A between C-alphas

    u = mda.Universe.empty(
        n_atoms, n_residues=n_atoms, atom_resindex=np.arange(n_atoms), trajectory=True
    )
    u.add_TopologyAttr("name", ["CA"] * n_atoms)
    u.add_TopologyAttr("resname", ["ALA"] * n_atoms)
    u.add_TopologyAttr("resid", np.arange(1, n_atoms + 1))
    u.add_TopologyAttr("chainID", ["A"] * n_atoms)
    u.add_TopologyAttr("element", ["C"] * n_atoms)
    u.add_TopologyAttr("occupancy", [1.0] * n_atoms)
    u.add_TopologyAttr("tempfactor", [0.0] * n_atoms)
    u.add_TopologyAttr("altLoc", [" "] * n_atoms)
    u.add_TopologyAttr("icode", [" "] * n_atoms)
    u.add_TopologyAttr("segid", [" "])
    u.add_TopologyAttr("record_type", ["ATOM"] * n_atoms)
    u.add_TopologyAttr("formalcharges", [0] * n_atoms)

    # Set dummy dimensions to avoid CRYST1 warnings [a, b, c, alpha, beta, gamma]
    u.dimensions = [100.0, 100.0, 100.0, 90.0, 90.0, 90.0]

    u.atoms.positions = coords

    u.atoms.write(path)
    return path


def test_full_simulation():
    pdb_path = "dummy.pdb"
    traj_path = (
        "output.pdb"  # Using .pdb for easy human reading if needed, but .dcd would be faster
    )

    try:
        create_dummy_pdb(pdb_path)

        system = System(pdb_path)
        ff = ANMForceField(system.equilibrium_coords, cutoff=10.0, spring_constant=1.0)
        integrator = LangevinIntegrator(dt=0.1, temperature=300.0, friction=1.0)
        sim = Simulation(system, ff, integrator)

        n_steps = 100
        stride = 10
        sim.run(n_steps=n_steps, output_path=traj_path, stride=stride)

        # Verify output
        assert os.path.exists(traj_path)
        u_out = mda.Universe(traj_path)
        # Expected frames: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90 -> 10 frames
        # MDAnalysis Writer might include the first frame depending on implementation.
        # Let's just check it's >= 10.
        print(f"Number of frames in output: {len(u_out.trajectory)}")
        assert len(u_out.trajectory) >= 10

    finally:
        if os.path.exists(pdb_path):
            os.remove(pdb_path)
        if os.path.exists(traj_path):
            os.remove(traj_path)


if __name__ == "__main__":
    test_full_simulation()
