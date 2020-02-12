"""
This module runs all the tests for the Neural Entity class
"""

import numpy as np

from simulating.action import Action
import simulating.entity as entity


def test_sigmoid():
    """
    Test sigmoid activation function on random array from normal distribution
    """

    x = np.random.randn(100)
    y = entity.sigmoid(x)
    assert (y > 0).all() and (y <= 1).all()


def test_relu():
    """
    Test relu activation function on random array from normal distribution
    """

    x = np.random.randn(100)
    y = entity.relu(x)
    assert (y >= 0).all()


def test_bits_to_array():
    """
    Test conversion from mushroom to array
    """

    mushroom = 0b0000011111
    mush_array = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    assert entity.bits_to_array(mushroom, 10) == mush_array


def test_array_to_bits():
    """
    Test conversion from mushroom to array
    """

    mushroom = 0b0000011111
    mush_array = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    assert entity.array_to_bits(mush_array) == mushroom


def test_initialise_parameters_size():
    """
    Test that parameters in the neural network for
    NeuralEntity are set with the right size
    """

    ent = entity.NeuralEntity(0, [5])
    assert len(ent.parameters) == 4
    assert ent.parameters["W1"].shape == (5, 14)
    assert ent.parameters["b1"].shape == (5, 1)
    assert ent.parameters["W2"].shape == (5, 5)
    assert ent.parameters["b2"].shape == (5, 1)


def test_forward_propogation_output_size():
    """
    Test that forward propogation through the entity's
    neural network returns a cache with appropriate weights
    """

    ent = entity.NeuralEntity(0, [5])
    inputs = np.array([0.5, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1])
    inputs = np.expand_dims(inputs, 1)
    outputs = ent.forward_propagation(inputs, linear=False)
    assert len(outputs) == 5


def test_behaviour_output_correct():
    """
    Test that the behaviour call outputs an action and a 3-bit vocal call
    """

    ent = entity.NeuralEntity(0, [5])
    action, vocal = ent.behaviour(0.4, 0b1111100000, [0, 1, 1])
    assert action in [
        Action.FORWARDS, Action.LEFT, Action.RIGHT, Action.NOTHING
    ]
    assert len(vocal) == 3
    for x in vocal:
        assert x in (0, 1)


def test_reproduce():
    """
    Test that reproduction creates offspring
    """

    ent = entity.NeuralEntity(100, [5])
    children = ent.reproduce(5, 0.5)
    assert len(children) == 5
    for child in children:
        assert child.energy == 0
        assert len(child.parameters) == len(ent.parameters)
