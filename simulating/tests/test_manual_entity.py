"""
This module runs all the tests for the ManualEntity class
"""

import simulating.entity as entity


def test_behaviour_forwards():
    """
    This tests that the manual behaviour returns a forwards action when
    the input location is 0.
    """

    ent = entity.ManualEntity()
    action, _ = ent.behaviour(0, 0b1111100000, (0, 1, 1))
    assert action == entity.Action.FORWARDS


def test_behaviour_right():
    """
    This tests that the manual behaviour returns a right action when
    the input location is between 0.25 and 0.5
    """

    ent = entity.ManualEntity()
    action, _ = ent.behaviour(0.375, 0b1111100000, (0, 1, 1))
    assert action == entity.Action.RIGHT


def test_behaviour_left():
    """
    This tests that the manual behaviour returns a left action when
    the input location is between 0.25 and 0.5
    """

    ent = entity.ManualEntity()
    action, _ = ent.behaviour(0.785, 0b1111100000, (0, 1, 1))
    assert action == entity.Action.LEFT


def test_behaviour_behind():
    """
    This tests that the manual behaviour returns either left or
    right action when the input location is exatly 0.5
    """

    ent = entity.ManualEntity()
    action, _ = ent.behaviour(0.5, 0b1111100000, (0, 1, 1))
    assert action in (entity.Action.LEFT or action, entity.Action.RIGHT)


def test_behaviour_output_vocal():
    """
    This tests that the manual behaviour returns an empty vocal response.
    """

    ent = entity.ManualEntity()
    _, vocal = ent.behaviour(0.5, 0b1111100000, (0, 1, 1))
    assert vocal == (0, 0, 0)
