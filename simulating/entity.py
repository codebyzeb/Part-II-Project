"""
Entity module manages the Entity class and the Action Enum.

The Entity class is used to represent individual creatures; specifically their energy
value and the behaviour method that decides on an Action given perceptual inputs.

The Action enum represents the entity's response of moving forwards, turning left
or right or doing nothing.

"""

import random

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

    def behaviour_manual(self, location):
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


# def behaviour_net(self, location, perception, listening):
#         """ Given perceptual inputs, uses the neural network to determine an action.

#         Args:
#             location (float): Location of the nearest mushroom in angle from 0 to 1.
#             perception: 10-bit properties of the adjacent mushroom
#             listening: Audio inputs
#         Returns:
#             (Action, vocal): An Action to be taken and the vocal response
#         """
