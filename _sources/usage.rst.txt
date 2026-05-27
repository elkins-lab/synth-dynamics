Usage Guide
===========

Installation
------------

Install the dependencies:

.. code-block:: bash

    pip install numpy MDAnalysis scipy

Running a Simulation
--------------------

A basic simulation involves defining a system, a forcefield, and an integrator.

.. code-block:: python

    from synth_dynamics import System, ANMForceField, LangevinIntegrator, Simulation

    # 1. Load the system (C-alpha atoms)
    system = System("protein.pdb")

    # 2. Define the Anisotropic Network Model forcefield
    ff = ANMForceField(system.equilibrium_coords, cutoff=15.0, spring_constant=1.0)

    # 3. Choose an integrator
    integrator = LangevinIntegrator(dt=0.1, temperature=300.0, friction=1.0)

    # 4. Run the simulation
    sim = Simulation(system, ff, integrator)
    sim.run(n_steps=1000, output_path="trajectory.dcd", stride=10)

Key Components
--------------

* **System**: Handles PDB loading and coordinate management.
* **ANMForceField**: Computes harmonic forces based on the Elastic Network Model.
* **LangevinIntegrator**: Propagates coordinates using the overdamped Langevin equation.
* **Simulation**: Orchestrates the run and writes output trajectories.
