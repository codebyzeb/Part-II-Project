"""
This module runs all the tests for the Entity class
"""

import simulating.entity as entity


def test_initial_energy():
    """
    This tests that the initial energy is set in the constructor
    """

    ent = entity.Entity(4)
    assert ent.energy == 4


def test_eat_two_poisonous():
    """
    This tests that the energy value is set correctly when eating two
    poisonous mushrooms.
    """

    ent = entity.Entity()
    ent.eat(0b1111100000)
    ent.eat(0b1111100001)
    assert ent.energy == 2 * entity.ENERGY_POISON


def test_eat_two_edible():
    """
    This tests that the energy value is set correctly when eating two
    edible mushrooms.
    """

    ent = entity.Entity()
    ent.eat(0b0000011111)
    ent.eat(0b0000111111)
    assert ent.energy == 2 * entity.ENERGY_EDIBLE


def test_eat_one_of_each():
    """
    This tests that the energy value is set correctly when eating two
    different mushrooms.
    """

    ent = entity.Entity()
    ent.eat(0b1111100000)
    ent.eat(0b0000011111)
    assert ent.energy == entity.ENERGY_EDIBLE + entity.ENERGY_POISON


def test_behaviour():
    """
    Ensures that the default behaviour is to return Nothing
    """

    ent = entity.Entity()
    action, _ = ent.behaviour()
    assert action == entity.Action.NOTHING
