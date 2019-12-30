"""
Entity module manages the Entity class and the Action Enum.

The Entity class is used to represent individual creatures; specifically their energy
value and the behaviour method that decides on an Action given perceptual inputs.

The Action enum represents the entity's response of moving forwards, turning left
or right or doing nothing.

"""

import copy
import random

import numpy as np

from simulating.action import Action
from simulating import environment

ENERGY_POISON = -11
ENERGY_EDIBLE = 10


class Entity:
    """ Representation of an Entity

    Attributes:
        energy: The current energy of this entity.
    """

    energy = 0

    def __init__(self, startEnergy=0):
        """ Instantiation of an Entity

        Args:
            startEnergy: The initial energy of this entity.
        """
        self.energy = startEnergy

    def eat(self, mushroom):
        """ Eat a mushroom
        
        The energy value changes according to whether or not the mushroom is edible.

        Args:
            mushroom: The mushroom to be eaten
        """

        if environment.is_edible(mushroom):
            self.energy += ENERGY_EDIBLE
        elif environment.is_poisonous(mushroom):
            self.energy += ENERGY_POISON

    def behaviour(self, location, perception, listening):  #pylint: disable=W0613
        """ Given perceptual inputs, returns an action.

        Args:
            location (float): Location of the nearest mushroom in angle from 0 to 1.
            perception: 10-bit properties of the adjacent mushroom
            listening: Audio inputs
        Returns:
            (Action, vocal): An Action to be taken and the vocal response
        """
        return Action.NOTHING, [0, 0, 0]


class ManualEntity(Entity):
    """ An entity that just moves to the closest mushroom
    """
    def behaviour(self, location, perception, listening):
        """ Given perceptual inputs, just moves towards and eats the nearest mushroom.

        Args:
            location (float): Location of the nearest mushroom in angle from 0 to 1.
            perception: 10-bit properties of the adjacent mushroom
            listening: Audio inputs
        Returns:
            (Action, vocal): An Action to be taken and the vocal response
        """

        action = Action.NOTHING

        if (location + 0.125) % 1 < 0.25:
            action = Action.FORWARDS

        elif location < 0.5:
            action = Action.RIGHT

        elif location > 0.5:
            action = Action.LEFT

        else:
            if random.randrange(0, 2) == 0:
                action = Action.LEFT
            else:
                action = Action.RIGHT

        return action, (0, 0, 0)


def sigmoid(z):
    """ Performs the sigmoid function on a vector to squash to [0,1]
    """
    return 1 / (1 + np.exp(-z))


def relu(z):
    """ Performs the Rectified Linear Unit activation function (clamps negative value to 0)
    """
    return np.multiply(z, z > 0)


def bits_to_array(num, output_size):
    """ Converts a number from an integer to an array of bits
    """

    ##list(map(int,bin(mushroom)[2:].zfill(output_size)))

    bit_array = []
    for i in range(output_size - 1, -1, -1):
        bit_array.append((num & (1 << i)) >> i)
    return bit_array


def array_to_bits(bit_array):
    """ Converts a bit array to an integer
    """
    num = 0
    for i, bit in enumerate(bit_array):
        num += int(bit) << (len(bit_array) - i - 1)
    return num


class NeuralEntity(Entity):
    """ An entity controlled by a Feed Forward Neural Network
    """

    parameters = {}

    def __init__(self, energy=0, hidden_units=[5]):  #pylint: disable=W0102
        super().__init__(energy)
        # Add 14 input units and 5 output units
        self.initialise_parameters([14] + hidden_units + [5])

    def initialise_parameters(self, layers_units):
        """ Initialises weights and biases of the neural network.

        Weights are initially set to 0

        Args:
            layer_units: The number of units in each layer
        """

        for layer in range(1, len(layers_units)):
            # Set all weights to 0
            self.parameters['W' + str(layer)] = np.zeros(
                (layers_units[layer], layers_units[layer - 1]))
            # Set all biases to 0
            self.parameters['b' + str(layer)] = np.zeros(
                (layers_units[layer], 1))

    def forward_propagation(self, inputs, linear):
        """ Given an input matrix, feeds it forwards through the neural network.

        Uses the relu activation function within the
        network and the sigmoid function for the output.

        Args:
            inputs: The input matrix for the network
            linear: Determines whether the output is linear or uses the sigmoid function
        Returns:
            cache: The activations of each node within the network
        """

        cache = {}
        final_layer = len(self.parameters) // 2
        cache["A0"] = inputs

        # For each layer, calculate the weight sum (Z) and the activation (A)
        for layer in range(1, final_layer):
            cache['Z' +
                  str(layer)] = (np.dot(self.parameters['W' + str(layer)],
                                        cache['A' + str(layer - 1)]) +
                                 self.parameters['b' + str(layer)])
            cache['A' + str(layer)] = relu(cache['Z' + str(layer)])

        # Calculate the final layer using the sigmoid function (or not)
        cache['Z' + str(final_layer)] = (
            np.dot(self.parameters['W' + str(final_layer)],
                   cache['A' + str(final_layer - 1)]) +
            self.parameters['b' + str(final_layer)])
        cache['A' +
              str(final_layer)] = (cache['Z' + str(final_layer)] if linear else
                                   sigmoid(cache['Z' + str(final_layer)]))
        return cache

    def reproduce(self, num_offspring, percentage_mutate):
        """ Produce children through asexual reproduction with random mutation

        A specified percentage of the weights are mutated in the children, by
        adding a value taken from the rectangular distribution [-1, 1].

        Args:
            num_offspring: The number of children to produce
            percentage_mutate: The percentage of weights to be mutated
        Returns:
            children: An array of children produced
        """

        children = []

        for _ in range(num_offspring):
            # Do a deep copy of self
            child = NeuralEntity(0)
            child.parameters = copy.deepcopy(self.parameters)
            num_layers = len(self.parameters) // 2 + 1

            # Randomly alter a percentage of the weights by adding a value in [-1, 1]
            for layer in range(1, num_layers):
                weights = child.parameters['W' + str(layer)]
                weights = np.array([[
                    x + random.random() * 2 -
                    1 if random.random() < percentage_mutate else x for x in xs
                ] for xs in weights])
                child.parameters['W' + str(layer)] = weights

            for layer in range(1, num_layers):
                biases = child.parameters['b' + str(layer)]
                biases = np.array([[
                    x + random.random() * 2 -
                    1 if random.random() < percentage_mutate else x for x in xs
                ] for xs in biases])
                child.parameters['b' + str(layer)] = biases

            # Add child to output
            children.append(child)

        return children

    def behaviour(self, location, perception, listening):
        """ Given perceptual inputs, just moves towards and eats the nearest mushroom.

        Args:
            location (float): Location of the nearest mushroom in angle from 0 to 1.
            perception: 10-bit properties of the adjacent mushroom
            listening: Audio inputs
        Returns:
            (Action, vocal): An Action to be taken and the vocal response
        """

        # Create neural network inputs
        inputs = []
        inputs.append(location)
        inputs.extend(bits_to_array(perception, 10))
        inputs.extend(listening)
        inputs = np.array([[inp] for inp in inputs])

        # Feed forward through the neural network
        cache = self.forward_propagation(inputs, linear=False)

        # Get outputs
        final_layer = len(self.parameters) // 2
        outputs = list(
            map(round, list(np.squeeze(cache['A' + str(final_layer)]))))

        # Debug info
        # print("Inputs to neural net: ", inputs)
        # print("Outputs from neural net: ", outputs)

        # Get action from outputs
        if (outputs[0] == 1 and outputs[1] == 1):
            action = Action.FORWARDS
        elif (outputs[0] == 1 and outputs[1] == 0):
            action = Action.LEFT
        elif (outputs[0] == 0 and outputs[1] == 1):
            action = Action.RIGHT
        else:
            action = Action.NOTHING

        # Get vocal from outputs
        vocal = array_to_bits(outputs[2:5])

        return action, vocal
