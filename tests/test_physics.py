import numpy as np
import pytest

from synth_dynamics import ANMForceField, LangevinIntegrator


def test_einstein_smoluchowski_diffusion() -> None:
    """
    Verifies that a free particle (k=0) follows the Einstein-Smoluchowski relation:
    MSD(t) = 6 * D * t, where D = kb * T / gamma.
    """
    dt = 0.5
    T = 300.0
    gamma = 5.0
    integrator = LangevinIntegrator(dt=dt, temperature=T, friction=gamma)

    # D = (0.001987 * 300) / 5.0 = 0.11922
    D = (integrator.kb * T) / gamma

    n_atoms = 100
    n_steps = 1000

    # Initialize atoms at origin
    positions = np.zeros((n_atoms, 3))
    forces = np.zeros((n_atoms, 3))

    sq_displacements = []

    current_pos = positions.copy()
    for _ in range(n_steps):
        current_pos = integrator.step(current_pos, forces)
        # Calculate MSD for this time step
        msd = np.mean(np.sum((current_pos - positions) ** 2, axis=1))
        sq_displacements.append(msd)

    # Total time elapsed
    times = np.arange(1, n_steps + 1) * dt

    # Perform linear fit: MSD = slope * t
    slope, _ = np.polyfit(times, sq_displacements, 1)

    # Theoretical slope is 6 * D
    expected_slope = 6.0 * D

    # Check within 5% tolerance (stochastic)
    assert np.isclose(slope, expected_slope, rtol=0.05)


def test_equipartition_harmonic_oscillator() -> None:
    """
    Verifies the Equipartition Theorem for a single harmonic bond.
    <V> = 1/2 * kb * T per degree of freedom.
    For a 1D harmonic oscillator: <1/2 * k * x^2> = 1/2 * kb * T.
    """
    # Parameters
    k = 5.0
    T = 300.0
    gamma = 10.0
    dt = 0.01

    integrator = LangevinIntegrator(dt=dt, temperature=T, friction=gamma)

    # System: Two atoms, one fixed at origin, one moving in 1D (x-axis)
    # R0 = 0
    # Force on moving atom: F = -k * x

    n_steps = 50000
    x = 1.0  # Initial displacement

    potential_energies = []

    for _ in range(n_steps):
        # Force: F = -k * x (in 1D)
        force = np.array([[-k * x, 0.0, 0.0]])
        pos = np.array([[x, 0.0, 0.0]])

        # Step
        new_pos = integrator.step(pos, force)
        x = new_pos[0, 0]

        # V = 1/2 * k * x^2
        potential_energies.append(0.5 * k * x**2)

    # Mean potential energy should be 1/2 * kb * T (for 1 degree of freedom)
    mean_v = np.mean(potential_energies[1000:])  # Burn-in
    expected_v = 0.5 * integrator.kb * T

    # Check within 10% (stochastic 1D sampling requires more steps for higher precision)
    assert np.isclose(mean_v, expected_v, rtol=0.1)


def test_boltzmann_distribution_bond() -> None:
    """
    Verifies that the distance distribution of a harmonic bond follows
    the Boltzmann distribution: P(r) ~ exp(-k(r-r0)^2 / 2kbT).
    This implies the variance of r should be kbT / k.
    """
    k = 2.0
    T = 500.0
    gamma = 5.0
    dt = 0.05
    r0 = 10.0

    integrator = LangevinIntegrator(dt=dt, temperature=T, friction=gamma)

    # Two atoms at (0,0,0) and (10,0,0)
    coords_eq = np.array([[0.0, 0.0, 0.0], [r0, 0.0, 0.0]])
    ff = ANMForceField(coords_eq, cutoff=20.0, spring_constant=k)

    n_steps = 20000
    pos = coords_eq.copy()

    distances = []
    for _ in range(n_steps):
        forces = ff.compute_forces(pos)
        pos = integrator.step(pos, forces)

        dist = np.linalg.norm(pos[0] - pos[1])
        distances.append(dist)

    # Variance of distance r should be kb * T / k
    # This is an approximation for small fluctuations in 3D
    actual_var = np.var(distances[1000:])
    expected_var = integrator.kb * T / k

    # Check within 10%
    assert np.isclose(actual_var, expected_var, rtol=0.1)


if __name__ == "__main__":
    pytest.main([__file__])
