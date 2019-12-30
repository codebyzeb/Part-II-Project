"""
Module for running simulation experiments.
"""

import cProfile
import sys

from multiprocessing import Process

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

    sim = simulation.Simulation(15, 50, 100, 1000)
    sim.run_population("testing",
                       language_type,
                       interactive=True,
                       record_language=True)


def neural_population_debug_simulation_5(language_type):
    """ Run a neural simulation for debugging
    """

    sim = simulation.Simulation(15, 50, 5, 1000)
    sim.run_population("testing",
                       language_type,
                       interactive=True,
                       record_language=True)


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

    sim = simulation.Simulation(15, 50, 100, 1000)
    sim.run_population(filename,
                       language_type,
                       interactive=False,
                       record_language=True)


def run_full_simulations(filenumber):
    """ Run a three full simulations in parallel for each language type
    """
    p1 = Process(target=neural_population_simulation_1000,
                 args=("output/external" + filenumber, "External"))
    p2 = Process(target=neural_population_simulation_1000,
                 args=("output/evolved" + filenumber, "Evolved"))
    p3 = Process(target=neural_population_simulation_1000,
                 args=("output/none" + filenumber, "None"))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()


if __name__ == "__main__":
    #run_full_simulations(str(sys.argv[1]))
    #neural_population_debug_simulation_1000("Evolved")
    #neural_population_debug_simulation_5("External")
    #cProfile.run("neural_population_debug_simulation_1()")
    neural_population_simulation_1000(
        "output-50/" + str(sys.argv[2]) + str(sys.argv[1]), str(sys.argv[2]))
