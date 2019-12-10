"""
Module for running simulation experiments.
"""

import cProfile

import simulating.simulation as simulation
import simulating.entity as entity


def basic_single_debug_simulation():
    """ Run a basic simulation for debugging.
    """

    sim = simulation.Simulation(5, 50, 100, 1000)
    sim.run_single(entity.ManualEntity())


def neural_single_debug_simulation():
    """ Run a neural simulation for debugging
    """

    ent = entity.NeuralEntity()
    print(ent.parameters)
    sim = simulation.Simulation(5, 50, 100, 1000)
    sim.run_single(ent, interactive=True)


def neural_population_debug_simulation_1000(language_type):
    """ Run a neural simulation for debugging
    """

    sim = simulation.Simulation(15, 75, 100, 1000)
    sim.run_population("out.txt", language_type, interactive=True)


def neural_population_debug_simulation_1():
    """ Run a neural simulation for debugging
    """

    sim = simulation.Simulation(15, 75, 100, 1)
    sim.run_population(True)


def print_some_weights():
    """ Simply prints weights of children
    """

    ent = entity.NeuralEntity()
    children = ent.reproduce(5, 0.1)
    print("Entity weights: ")
    print(ent.parameters["W1"])
    print()
    print("Children weights: ")
    for child in children:
        print(child.parameters["W1"])
        print()


def neural_population_simulation_1000(filename, language_type):
    """ Run a full simulation for 1000 generations
    """

    sim = simulation.Simulation(15, 75, 100, 1000)
    sim.run_population(filename, language_type, interactive=False)


if __name__ == "__main__":
    neural_population_debug_simulation_1000("External")
    #cProfile.run("neural_population_debug_simulation_1()")
