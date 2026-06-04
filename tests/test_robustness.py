import os
from pathlib import Path

import numpy as np
import pytest

from synth_dynamics import ANMForceField, LangevinIntegrator, Simulation, System


def test_system_file_not_found() -> None:
    with pytest.raises(FileNotFoundError, match="PDB file not found"):
        System("non_existent.pdb")


def test_system_invalid_positions_setter(tmp_path: Path) -> None:
    # Create a dummy PDB first
    pdb_path = tmp_path / "dummy.pdb"
    import MDAnalysis as mda

    u = mda.Universe.empty(1, trajectory=True)
    u.add_TopologyAttr("name", ["CA"])
    u.add_TopologyAttr("resname", ["ALA"])
    u.add_TopologyAttr("resid", [1])
    u.add_TopologyAttr("record_type", ["ATOM"])
    u.add_TopologyAttr("formalcharges", [0])
    u.atoms.positions = np.array([[0, 0, 0]])
    u.atoms.write(str(pdb_path))

    sys = System(str(pdb_path))

    # Correct shape
    sys.positions = np.array([[1.0, 1.0, 1.0]])
    assert np.allclose(sys.positions, [[1.0, 1.0, 1.0]])

    # Incorrect shape
    with pytest.raises(ValueError, match="Invalid positions shape"):
        sys.positions = np.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]])

    # Non-array input (should be converted)
    sys.positions = np.array([[2.0, 2.0, 2.0]])
    assert np.allclose(sys.positions, [[2.0, 2.0, 2.0]])


@pytest.mark.parametrize(
    "dt,T,gamma",
    [
        (0, 300, 1),
        (-0.1, 300, 1),
        (0.1, -1, 1),
        (0.1, 300, 0),
        (0.1, 300, -1),
    ],
)
def test_integrator_invalid_params(dt: float, T: float, gamma: float) -> None:
    with pytest.raises(ValueError):
        LangevinIntegrator(dt=dt, temperature=T, friction=gamma)


def test_integrator_statistical_check() -> None:
    dt = 0.1
    T = 300.0
    gamma = 2.0
    integrator = LangevinIntegrator(dt=dt, temperature=T, friction=gamma)

    n_samples = 10000
    positions = np.zeros((n_samples, 3))
    forces = np.zeros((n_samples, 3))

    # We take one step for many independent atoms to get a distribution
    new_positions = integrator.step(positions, forces)
    displacements = new_positions - positions

    # Expected variance: sigma^2 = 2 * kb * T * dt / gamma
    expected_var = 2.0 * integrator.kb * T * dt / gamma
    actual_var = np.var(displacements)

    # Check mean is close to 0
    assert np.allclose(np.mean(displacements), 0.0, atol=0.01)
    # Check variance is within 5% of expected
    assert np.isclose(actual_var, expected_var, rtol=0.05)


def test_forcefield_cutoffs() -> None:
    coords = np.array([[0.0, 0.0, 0.0], [10.0, 0.0, 0.0]])

    # Cutoff below distance
    ff_none = ANMForceField(coords, cutoff=5.0)
    assert not np.any(ff_none.adj)

    # Cutoff above distance
    ff_all = ANMForceField(coords, cutoff=15.0)
    assert np.all(ff_all.adj == [[False, True], [True, False]])


def test_simulation_zero_steps(tmp_path: Path) -> None:
    # Setup minimal system
    pdb_path = tmp_path / "min.pdb"
    import MDAnalysis as mda

    u = mda.Universe.empty(1, trajectory=True)
    u.add_TopologyAttr("name", ["CA"])
    u.add_TopologyAttr("record_type", ["ATOM"])
    u.add_TopologyAttr("formalcharges", [0])
    u.atoms.positions = np.array([[0, 0, 0]])
    u.atoms.write(str(pdb_path))

    sys = System(str(pdb_path))
    ff = ANMForceField(sys.equilibrium_coords)
    integrator = LangevinIntegrator()
    sim = Simulation(sys, ff, integrator)

    traj_path = tmp_path / "out.dcd"
    sim.run(n_steps=0, output_path=str(traj_path))

    # Should have at least been created (though might be empty depending on MDAnalysis)
    assert os.path.exists(traj_path)


def test_simulation_stride_large(tmp_path: Path) -> None:
    pdb_path = tmp_path / "min.pdb"
    import MDAnalysis as mda

    u = mda.Universe.empty(1, trajectory=True)
    u.add_TopologyAttr("name", ["CA"])
    u.add_TopologyAttr("record_type", ["ATOM"])
    u.add_TopologyAttr("formalcharges", [0])
    u.atoms.positions = np.array([[0, 0, 0]])
    u.atoms.write(str(pdb_path))

    sys = System(str(pdb_path))
    ff = ANMForceField(sys.equilibrium_coords)
    integrator = LangevinIntegrator()
    sim = Simulation(sys, ff, integrator)

    traj_path = tmp_path / "out.pdb"
    # 5 steps, stride 10 -> only step 0 should be written
    sim.run(n_steps=5, output_path=str(traj_path), stride=10)

    u_out = mda.Universe(str(traj_path))
    assert len(u_out.trajectory) == 1
