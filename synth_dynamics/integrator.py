import numpy as np


class LangevinIntegrator:
    def __init__(self, dt: float = 0.1, temperature: float = 300.0, friction: float = 1.0) -> None:
        """
        Overdamped Langevin (Brownian) Integrator.

        Args:
            dt: Time step.
            temperature: Temperature in Kelvin.
            friction: Friction coefficient (gamma).
        """
        self.dt = dt
        self.T = temperature
        self.gamma = friction
        self.kb = 0.0019872041  # Boltzmann constant in kcal/(mol*K)

    def step(self, positions: np.ndarray, forces: np.ndarray) -> np.ndarray:
        """
        Performs a single integration step.

        x(t+dt) = x(t) + (dt/gamma) * F + sqrt(2 * kb * T * dt / gamma) * R

        Args:
            positions: (N, 3) array of current positions.
            forces: (N, 3) array of current forces.
        Returns:
            new_positions: (N, 3) array of updated positions.
        """
        n_atoms = positions.shape[0]

        # Deterministic term
        drift = (self.dt / self.gamma) * forces

        # Stochastic term
        sigma = np.sqrt(2.0 * self.kb * self.T * self.dt / self.gamma)
        random_force = sigma * np.random.normal(size=(n_atoms, 3))

        return np.asarray(positions + drift + random_force)
