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


def test_behaviour_manual_forwards():
    """
    This tests that the manual behaviour returns a forwards action when
    the input location is 0.
    """

    ent = entity.Entity()
    action, _ = ent.behaviour_manual(0)
    assert action == entity.Action.FORWARDS


def test_behaviour_manual_right():
    """
    This tests that the manual behaviour returns a right action when
    the input location is between 0.25 and 0.5
    """

    ent = entity.Entity()
    action, _ = ent.behaviour_manual(0.375)
    assert action == entity.Action.RIGHT


def test_behaviour_manual_left():
    """
    This tests that the manual behaviour returns a left action when
    the input location is between 0.25 and 0.5
    """

    ent = entity.Entity()
    action, _ = ent.behaviour_manual(0.785)
    assert action == entity.Action.LEFT


def test_behaviour_manual_behind():
    """
    This tests that the manual behaviour returns either left or
    right action when the input location is exatly 0.5
    """

    ent = entity.Entity()
    action, _ = ent.behaviour_manual(0.5)
    assert action == entity.Action.LEFT or action == entity.Action.RIGHT


def test_behaviour_manual_output_vocal():
    """
    This tests that the manual behaviour returns an empty vocal response.
    """

    ent = entity.Entity()
    _, vocal = ent.behaviour_manual(0.5)
    assert vocal == (0, 0, 0)
