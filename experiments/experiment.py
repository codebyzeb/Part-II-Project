"""
Module for running simulation experiments.
"""

import cProfile
import sys

import simulating.simulation as simulation
from simulating.simulation import Language
import simulating.entity as entity


def basic_single_debug_simulation():
    """ Run a basic simulation for debugging.
    """

    sim = simulation.Simulation(5, 50, 100, 1000, Language.NONE)
    sim.set_io_options(interactive=True, foldername="testing")
    sim.run_single(entity.ManualEntity(), viewer=True)


def neural_single_debug_simulation():
    """ Run a neural simulation for debugging
    """

    ent = entity.NeuralEntity()
    print(ent.parameters)
    sim = simulation.Simulation(5, 50, 100, 1000, Language.NONE)
    sim.set_io_options(interactive=True, foldername="testing")
    sim.run_single(ent, viewer=True)


def neural_population_debug_simulation_1000(language_type):
    """ Run a neural simulation for debugging
    """

    sim = simulation.Simulation(15, 50, 100, 1000, language_type)
    sim.set_io_options(interactive=True, foldername="testing")
    sim.start()


def neural_population_debug_simulation_5(language_type):
    """ Run a neural simulation for debugging
    """

    sim = simulation.Simulation(15, 50, 5, 1000, language_type)
    sim.set_io_options(foldername="testing", interactive=True)
    sim.start()


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


def neural_population_simulation_1000(foldername, language_type):
    """ Run a full simulation for 1000 generations
    """

    sim = simulation.Simulation(15, 50, 100, 1000, language_type)
    sim.set_io_options(foldername=foldername)
    sim.start()


def watch_old_simulation(foldername, language_type):
    """ Load a previous simulation to watch the entities
    """

    sim = simulation.Simulation(15, 50, 100, 1000, language_type)
    sim.set_io_options(interactive=True,
                       record_language=False,
                       record_entities=False,
                       foldername=foldername)


if __name__ == "__main__":
    #run_full_simulations(str(sys.argv[1]))
    #neural_population_debug_simulation_1000("Evolved")
    neural_population_debug_simulation_5("None")
    #cProfile.run("neural_population_debug_simulation_1()")
    #neural_population_simulation_1000(
    #    "output-50/" + str(sys.argv[2]) + str(sys.argv[1]), str(sys.argv[2]))
