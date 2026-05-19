import numpy as np
import pytest
from synth_dynamics import System, ANMForceField, LangevinIntegrator

def test_forcefield_equilibrium():
    # Two atoms at (0,0,0) and (10,0,0)
    coords = np.array([[0.0, 0.0, 0.0], [10.0, 0.0, 0.0]])
    ff = ANMForceField(coords, cutoff=15.0, spring_constant=1.0)
    
    # Forces at equilibrium should be zero
    forces = ff.compute_forces(coords)
    assert np.allclose(forces, 0.0)

def test_forcefield_displacement():
    # Two atoms at (0,0,0) and (10,0,0)
    coords_eq = np.array([[0.0, 0.0, 0.0], [10.0, 0.0, 0.0]])
    ff = ANMForceField(coords_eq, cutoff=15.0, spring_constant=1.0)
    
    # Displace one atom to (11,0,0)
    coords_new = np.array([[0.0, 0.0, 0.0], [11.0, 0.0, 0.0]])
    forces = ff.compute_forces(coords_new)
    
    # Force on atom 0 should be in +x direction (restoring towards atom 1)
    # F0 = -k * (r - r0) * (r0 - r1) / r = -1.0 * (11 - 10) * ([0-11, 0, 0]) / 11 
    # Wait, my implementation: F_i = sum_j -k * (dist_ij - r0_ij) * (diff_ij / dist_ij)
    # diff_ij = r_i - r_j
    # F0 = -1.0 * (11 - 10) * ([0-11, 0, 0] / 11) = -1.0 * 1 * [-1, 0, 0] = [1, 0, 0]
    # F1 = -1.0 * (11 - 10) * ([11-0, 0, 0] / 11) = -1.0 * 1 * [1, 0, 0] = [-1, 0, 0]
    
    assert np.allclose(forces[0], [1.0, 0.0, 0.0])
    assert np.allclose(forces[1], [-1.0, 0.0, 0.0])

def test_integrator_drift():
    integrator = LangevinIntegrator(dt=1.0, temperature=0.0, friction=1.0)
    positions = np.array([[0.0, 0.0, 0.0]])
    forces = np.array([[1.0, 0.0, 0.0]])
    
    # At T=0, x_new = x + (dt/gamma) * F = 0 + (1/1) * 1 = 1
    new_positions = integrator.step(positions, forces)
    assert np.allclose(new_positions, [[1.0, 0.0, 0.0]])

def test_system_no_ca(tmp_path):
    # Create a PDB with no CA atoms
    pdb_path = tmp_path / "no_ca.pdb"
    import MDAnalysis as mda
    u = mda.Universe.empty(1, trajectory=True)
    u.add_TopologyAttr('name', ['H'])
    u.atoms.write(str(pdb_path))
    
    with pytest.raises(ValueError, match="No C-alpha atoms found"):
        System(str(pdb_path))

def test_integrator_stochastic():
    # At T > 0, multiple steps should yield different positions due to noise
    integrator = LangevinIntegrator(dt=0.1, temperature=300.0, friction=1.0)
    positions = np.array([[0.0, 0.0, 0.0]])
    forces = np.array([[0.0, 0.0, 0.0]])
    
    pos1 = integrator.step(positions, forces)
    pos2 = integrator.step(positions, forces)
    
    assert not np.allclose(pos1, pos2)
    assert not np.allclose(pos1, positions)

if __name__ == "__main__":
    pytest.main([__file__])
