"""
This module runs all the tests for the Simulation class
"""

import pickle
import shutil

from simulating.simulation import Simulation
from simulating.simulation import Language
from simulating.entity import Entity
from simulating.entity import NeuralEntity


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


def test_get_signal_evolved():
    """
    Test that getting the signal for a population with evolved
    language gives the signal of the population entity provided
    """

    sim = Simulation(4, 5, 6, 7, "Evolved")
    angle = 0
    mush = 0b1111100000
    partner = NeuralEntity()
    population = [partner]
    viewer = False
    _, partner_signal = partner.behaviour(angle, mush, [0.5, 0.5, 0.5])

    signal = sim.get_signal(angle, mush, population, viewer)
    assert signal == partner_signal


def test_reproduce_population():
    """
    Test that reproducing a population produces a new population
    """

    sim = Simulation(4, 5, 10, 7, "External")
    entities = [NeuralEntity(100) for _ in range(10)]
    new_entities = sim.reproduce_population(entities)
    for entity in new_entities:
        assert entity.fitness == 0
    assert len(entities) == len(new_entities)


def test_naming_task():
    """
    Tests that a naming task produces the correct number of samples in the correct range
    """

    sim = Simulation(4, 5, 6, 7, "None")
    entity = NeuralEntity()
    edible, poisonous = sim.naming_task(entity)
    assert len(edible) == 40
    assert len(poisonous) == 40
    for s in edible:
        assert s in list(range(0, 8))
    for s in poisonous:
        assert s in list(range(0, 8))


def test_naming_task_all_zero():
    """
    Tests that a naming task on Entities (which always return 0 as a signal) produces correct samples
    """

    sim = Simulation(4, 5, 6, 7, "None")
    entity = Entity()
    edible, poisonous = sim.naming_task(entity)
    assert len(edible) == 40
    assert len(poisonous) == 40
    for s in edible:
        assert s == 0
    for s in poisonous:
        assert s == 0


def test_save_language():
    """
    Test that saving a language produces a file with a valid language frequency table
    """

    sim = Simulation(4, 5, 6, 5, "None")
    sim.set_io_options(foldername="testing")
    sim.initialise_io()
    sim.start()
    languages = pickle.load(open("testing/language.p", "rb"))
    shutil.rmtree('testing')
    assert len(languages) == 6
    for i in range(6):
        assert len(languages[i]) == 2
        assert len(languages[i]["edible"]) == 8
        assert len(languages[i]["poisonous"]) == 8
        assert abs(sum(languages[i]["edible"]) - 1) < 1e-5
        assert abs(sum(languages[i]["poisonous"]) - 1) < 1e-5


def test_save_load_entity():
    """
    Test that saving and loading a population returns the same population
    """

    sim = Simulation(4, 5, 6, 7, "None")
    sim.set_io_options(foldername="testing")
    sim.initialise_io()
    population = [NeuralEntity() for _ in range(100)]
    sim.save_entities(population, 0)
    new_entities = sim.load_entities(0)
    shutil.rmtree('testing')
    for i, e in enumerate(new_entities):
        assert e.equal_network(population[i])
