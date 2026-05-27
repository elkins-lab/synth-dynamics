"""
Example script for running a coarse-grained ENM Langevin simulation.
"""


def main():
    # In a real scenario, you would provide a PDB path
    # pdb_path = "path/to/your/protein.pdb"

    print("This is an example script. Please provide a PDB file to run a real simulation.")
    print("Usage:")
    print("system = System('protein.pdb')")
    print("ff = ANMForceField(system.equilibrium_coords, cutoff=15.0)")
    print("integrator = LangevinIntegrator(dt=0.1, temperature=300.0)")
    print("sim = Simulation(system, ff, integrator)")
    print("sim.run(n_steps=1000, output_path='trajectory.dcd', stride=10)")


if __name__ == "__main__":
    main()
