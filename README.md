# synth-dynamics: Time-Resolved Ensemble Generator

`synth-dynamics` is a fast, lightweight molecular dynamics engine designed to generate meaningful conformational ensembles of proteins. Unlike full-atom simulations (like GROMACS or Amber), `synth-dynamics` uses a **Coarse-Grained Anisotropic Network Model (ANM)** and **Langevin dynamics** to capture the essential global motions of proteins with minimal computational overhead.

This tool is designed to bridge the gap between static structures and time-averaged experimental observables, such as NMR relaxation parameters, SAXS Kratky plots, or FRET efficiency distributions.

## Key Features

- **Coarse-Grained Simulation**: Models proteins using C-alpha atoms and harmonic "spring" networks.
- **Fast Langevin Engine**: Propagates coordinates using a stable, overdamped Langevin integrator.
- **Experimental Integration**: Perfect for generating the structural ensembles needed for `synth-nmr` or `synth-saxs`.
- **Easy to Use**: Simple API for loading PDBs, configuring forcefields, and running simulations.
- **Extensively Tested**: 100% test coverage ensuring reliability and correctness.

## Installation

`synth-dynamics` requires Python 3.10+ and the following dependencies:

```bash
pip install numpy MDAnalysis scipy
```

To install the documentation theme:
```bash
pip install sphinx_rtd_theme
```

## Quick Start

Running a simulation is straightforward:

```python
from synth_dynamics import System, ANMForceField, LangevinIntegrator, Simulation

# 1. Load the system (automatically filters for C-alpha atoms)
system = System("protein.pdb")

# 2. Define the Anisotropic Network Model forcefield
# Cutoff (15A) and spring constant determine the flexibility
ff = ANMForceField(system.equilibrium_coords, cutoff=15.0, spring_constant=1.0)

# 3. Initialize the Langevin integrator (dt in fs, T in Kelvin)
integrator = LangevinIntegrator(dt=0.1, temperature=300.0, friction=1.0)

# 4. Run and save the trajectory
sim = Simulation(system, ff, integrator)
sim.run(n_steps=1000, output_path="trajectory.dcd", stride=10)
```

## Documentation

Full API documentation and usage guides are available in the `docs/` directory. You can build the HTML documentation locally:

```bash
cd docs
sphinx-build -b html . _build/html
```

## Testing

To run the test suite and verify coverage:

```bash
PYTHONPATH=. pytest --cov=synth_dynamics tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details (if applicable).
