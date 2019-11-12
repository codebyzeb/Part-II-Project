"""
Module for running simulation experiments.
"""

import simulating.simulation as simulation
import simulating.entity as entity

import cProfile


def basic_single_debug_simulation():
    """ Run a basic simulation for debugging.
    """

    sim = simulation.Simulation(5, 50, 100, 1000)
    sim.run_single(entity.ManualEntity(), debug=True)


def neural_single_debug_simulation():
    """ Run a neural simulation for debugging
    """

    ent = entity.NeuralEntity()
    print(ent.parameters)
    sim = simulation.Simulation(5, 50, 100, 1000)
    sim.run_single(ent, debug=True)


def neural_population_debug_simulation_1000():
    """ Run a neural simulation for debugging
    """

    sim = simulation.Simulation(15, 75, 100, 1000)
    sim.run_population(debug=True)


def neural_population_debug_simulation_1():
    """ Run a neural simulation for debugging
    """

    sim = simulation.Simulation(15, 75, 100, 1)
    sim.run_population(debug=True)


def print_some_weights():

    ent = entity.NeuralEntity()
    children = ent.reproduce(5, 0.1)
    print("Entity weights: ")
    print(ent.parameters["W1"])
    print()
    print("Children weights: ")
    for child in children:
        print(child.parameters["W1"])
        print()


if __name__ == "__main__":
    neural_population_debug_simulation_1000()
    #cProfile.run("neural_population_debug_simulation_1()")
