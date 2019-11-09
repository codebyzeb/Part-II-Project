import simulating.simulation as simulation
import simulating.entity as entity

sim = simulation.Simulation(5, 50, entity.Entity())
sim.run(debug=True)