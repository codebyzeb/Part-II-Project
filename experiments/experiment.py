"""
Module for running simulation experiments.
"""

import simulating.simulation as simulation
import simulating.entity as entity


def basic_debug_simulation():
    """ Run a basic simulation for debugging.
    """

    sim = simulation.Simulation(5, 50, entity.Entity())
    sim.run(debug=True)


if __name__ == "__main__":
    basic_debug_simulation()
