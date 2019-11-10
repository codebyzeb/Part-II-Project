"""
Module for running simulation experiments.
"""

import simulating.simulation as simulation
import simulating.entity as entity


def basic_debug_simulation():
    """ Run a basic simulation for debugging.
    """

    sim = simulation.Simulation(5, 50, entity.ManualEntity())
    sim.run(debug=True)


def neural_debug_simulation():
    """ Run a neural simulation for debugging
    """

    ent = entity.NeuralEntity()
    print(ent.parameters)
    sim = simulation.Simulation(5, 50, ent)
    sim.run(debug=True)


if __name__ == "__main__":
    neural_debug_simulation()
