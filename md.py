"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory

def calcenergy(a):
    
    """Function to print the potential, kinetic and total energy."""
    epot = 0
    ekin = a.get_kinetic_energy() / len(a)

    return {"epot":epot, "ekin":ekin, "T":ekin / (1.5 * units.kB), "etot": epot + ekin} 
#Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
#           'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))

    

def run_md():

    # Use Asap for a huge performance increase if it is installed
    use_asap = True

    if use_asap:
        from asap3 import EMT
        size = 10
    else:
        from ase.calculators.emt import EMT
        size = 3

    # Set up a crystal
    atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                            symbol="Cu",
                            size=(size, size, size),
                            pbc=True)

    # Describe the interatomic interactions with the Effective Medium Theory
    atoms.calc = EMT()

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=300)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.
    traj = Trajectory("cu.traj", "w", atoms)
    dyn.attach(traj.write, interval=10)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        calculated_energy = calcenergy(a)
        print('energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
           'Etot = %.3feV' % (calculated_energy['epot'], calculated_energy['ekin'], calculated_energy['T'], calculated_energy['etot']))

    
    # Now run the 
    dyn.attach(printenergy, interval=10)
    printenergy()
    dyn.run(200)

if __name__ == "__main__":
    run_md()
