"""
This module runs all the tests for the Simulation class
"""

import numpy as np

from simulating.simulation import Simulation
from simulating.simulation import Language
from simulating.entity import NeuralEntity as Entity


def test_new_simulation():
    """
    Test parameter setting of a new simulation
    """

    sim = Simulation(4, 5, 6, 7, "Evolved")
    assert sim.num_epochs == 4
    assert sim.num_cycles == 5
    assert sim.num_entities == 6
    assert sim.num_generations == 7
    assert sim.language_type == Language.EVOLVED


def test_io_params():
    """
    Test IO parameters set correctly
    """

    sim = Simulation(4, 5, 6, 7, "Evolved")
    sim.set_io_options(interactive=True,
                       record_language=False,
                       record_language_period=2,
                       record_entities=False,
                       record_entities_period=4,
                       record_fitness=False,
                       foldername="example")
    assert sim.interactive
    assert not sim.record_language
    assert sim.record_language_period == 2
    assert not sim.record_entities
    assert sim.record_entities_period == 4
    assert not sim.record_fitness
    assert sim.foldername == "example"


def test_get_signal_no_language():
    """
    Test that getting the signal for a population without language
    gives a constant signal
    """

    sim = Simulation(4, 5, 6, 7, "None")
    angle = 0
    mush = 0
    population = []
    viewer = False
    signal = sim.get_signal(angle, mush, population, viewer)
    assert signal == [0.5, 0.5, 0.5]


def test_get_signal_external_language_edible():
    """
    Test that getting the signal for a population with external
    language gives a specific signal for edible mushrooms
    """

    sim = Simulation(4, 5, 6, 7, "External")
    angle = 0
    mush = 0b0000011111
    population = []
    viewer = False
    signal = sim.get_signal(angle, mush, population, viewer)
    assert signal == [0, 1, 0]


def test_get_signal_external_language_poisonous():
    """
    Test that getting the signal for a population with external
    language gives a specific signal for edible mushrooms
    """

    sim = Simulation(4, 5, 6, 7, "External")
    angle = 0
    mush = 0b1111100000
    population = []
    viewer = False
    signal = sim.get_signal(angle, mush, population, viewer)
    assert signal == [1, 0, 0]


def test_reproduce_population():
    """
    Test that reproducing a population produces a new population
    """

    sim = Simulation(4, 5, 10, 7, "External")
    entities = [Entity(100) for _ in range(10)]
    new_entities = sim.reproduce_population(entities)
    for entity in new_entities:
        assert entity.fitness == 0
    assert len(entities) == len(new_entities)
