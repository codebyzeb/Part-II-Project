"""
Entity module manages the Entity class and the Action Enum.

The Entity class is used to represent individual creatures; specifically their fitness
value and the behaviour method that decides on an Action given perceptual inputs.

The Action enum represents the entity's response of moving forwards, turning left
or right or doing nothing.

"""

import copy
import random

import numpy as np

from simulating.action import Action
from simulating import environment

# Values gained from eating mushrooms
ENERGY_POISON = -11
ENERGY_EDIBLE = 10

# Control activation layers
ACTIVATION = "identity"
LINEAR = False


class Entity:
    """ Representation of an Entity

    Attributes:
        fitness: The current fitness of this entity.
    """
    def __init__(self, startFitness=0):
        """ Instantiation of an Entity

        Args:
            startFitness: The initial fitness of this entity.
        """
        self.fitness = startFitness

    def eat(self, mushroom):
        """ Eat a mushroom
        
        The fitness value changes according to whether or not the mushroom is edible.

        Args:
            mushroom: The mushroom to be eaten
        """

        if environment.is_edible(mushroom):
            self.fitness += ENERGY_EDIBLE
        elif environment.is_poisonous(mushroom):
            self.fitness += ENERGY_POISON

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

        return action, [0, 0, 0]


def sigmoid(z):
    """ Performs the sigmoid function on a vector to squash to [0,1]
    """
    return 1 / (1 + np.exp(np.clip(-z, -100, 100)))


def relu(z):
    """ Performs the Rectified Linear Unit activation function (clamps negative value to 0)
    """
    return np.multiply(z, z > 0)


def activation(z):
    """ Performs the activation function depending on the global parameter ACTIVATION
    """
    if ACTIVATION == "identity":
        return z
    if ACTIVATION == "sigmoid":
        return sigmoid(z)
    if ACTIVATION == "relu":
        return relu(z)


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

    weights = []
    biases = []

    def __init__(self, fitness=0, hidden_units=[5]):  #pylint: disable=W0102
        super().__init__(fitness)
        # Add 14 input units and 5 output units
        self.weights = [None]
        self.biases = [None]
        self.initialise_parameters([14] + hidden_units + [5])

    def initialise_parameters(self, layers_units, zero=False):
        """ Initialises weights and biases of the neural network.

        Weights are initially set to random values

        Args:
            layer_units: The number of units in each layer
            zero: Sets weights and biases to 0
        """

        for layer in range(1, len(layers_units)):
            # Choose random weights and biases from rectangular distribution [-1, 1]
            layer_weights = (2 * np.random.random_sample(
                (layers_units[layer], layers_units[layer - 1])) - 1)
            self.weights.append(layer_weights)

            layer_biases = (2 * np.random.random_sample((layers_units[layer], 1)) - 1)
            self.biases.append(layer_biases)

        # Initialise the parameters to zero
        if zero:
            for layer in range(1, len(layers_units)):
                # Set all weights and biases to 0
                self.weights[layer] = np.zeros((layers_units[layer], layers_units[layer - 1]))
                self.biases[layer] = np.zeros((layers_units[layer], 1))

    def forward_propagation(self, inputs):
        """ Given an input matrix, feeds it forwards through the neural network.

        Uses the relu activation function within the
        network and the sigmoid function for the output.

        Args:
            inputs: The input matrix for the network
        Returns:
            outputs: The activations of the final layer within the network
        """

        num_layers = len(self.weights)
        activations = [None for _ in range(num_layers)]
        activations[0] = inputs

        # For each layer, calculate the weighted sum (Z) and the activations
        for layer in range(1, num_layers - 1):
            Z = np.dot(self.weights[layer], activations[layer - 1]) + self.biases[layer]
            # Perform activation function
            activations[layer] = activation(Z)

        # Calculate the final layer using the sigmoid function (or not)
        Z = np.dot(self.weights[-1], activations[-2]) + self.biases[-1]
        activations[-1] = Z if LINEAR else sigmoid(Z)

        # Return final layer, rounded to 0 or 1
        outputs = list(map(int, map(round, list(np.squeeze(activations[-1])))))
        outputs = [1 if x >= 1 else 0 for x in outputs]

        return outputs

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
            child.weights = copy.deepcopy(self.weights)
            child.biases = copy.deepcopy(self.biases)
            num_layers = len(self.weights)

            # Randomly alter a percentage of the weights by adding a value in [-1, 1]
            for layer in range(1, num_layers):
                weights = child.weights[layer]
                weights = np.array([[
                    x + random.random() * 2 - 1 if random.random() < percentage_mutate else x
                    for x in xs
                ] for xs in weights])
                child.weights[layer] = weights

            for layer in range(1, num_layers):
                biases = child.biases[layer]
                biases = np.array([[
                    x + random.random() * 2 - 1 if random.random() < percentage_mutate else x
                    for x in xs
                ] for xs in biases])
                child.biases[layer] = biases

            # Add child to output
            children.append(child)

        return children

    def behaviour(self, location, perception, listening):
        """ Given perceptual inputs, just moves towards and eats the nearest mushroom.

        Args:
            location (float): Location of the nearest mushroom in angle from 0 to 1.
            perception: 10-bit properties of the adjacent mushroom
            listening (float[]): Audio inputs
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
        outputs = self.forward_propagation(inputs)

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
        vocal = outputs[2:5]

        return action, vocal

    def copy(self):
        """
        Returns a copy of this entity with default fitness
        """

        ent = NeuralEntity()
        ent.weights = copy.deepcopy(self.weights)
        ent.biases = copy.deepcopy(self.biases)
        return ent

    def equal_network(self, ent):
        """
        Returns whether the weights and biases of these two entities are equal
        """

        if not (len(self.weights) == len(ent.weights) and len(self.biases) == len(ent.biases)):
            return False

        for i, w in enumerate(self.weights):
            if w is None and not ent.weights[i] is None:
                return False
            if not w is None and ent.weights[i] is None:
                return False
            if w is None and ent.weights[i] is None:
                continue
            if not (w == ent.weights[i]).all():
                return False
        for i, b in enumerate(self.biases):
            if b is None and not ent.biases[i] is None:
                return False
            if not b is None and ent.biases[i] is None:
                return False
            if b is None and ent.biases[i] is None:
                continue
            if not (b == ent.biases[i]).all():
                return False

        return True
