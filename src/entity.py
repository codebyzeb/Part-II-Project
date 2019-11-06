from enum import Enum
import environment
import random

"""
Entity module manages the Entity class and the Action Enum.

The Entity class is used to represent individual creatures; specifically their energy
value and the behaviour method that decides on an action given perceptual inputs.

The ACTION enum represents the entity's response of moving forwards, turning left
or right or doing nothing.

"""

ENERGY_POISON = -11
ENERGY_EDIBLE = 10

class ACTION(Enum):
    """ Representation of an Action
    """

    FORWARDS = 0b11
    LEFT = 0b10
    RIGHT = 0b01
    NOTHING = 0b00

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

        if (environment.isEdible(mushroom)):
            self.energy += ENERGY_EDIBLE
        elif (environment.isPoisonous(mushroom)):
            self.energy += ENERGY_POISON

    def behaviourManual(self, location, perception, listening):
        """ Given perceptual inputs, just moves towards and eats the nearest mushroom.

        Args:
            location (float): Location of the nearest mushroom in angle from 0 to 1.
            perception: 10-bit properties of the adjacent mushroom
            listening: Audio inputs
        Returns:
            (action, vocal): An action to be taken and the vocal response
        """

        action = ACTION.NOTHING

        if ((location + 0.125) % 1 < 0.25):
            action = ACTION.FORWARDS
        
        elif (location < 0.5):
            action = ACTION.RIGHT

        elif (location > 0.5):
            action = ACTION.LEFT

        else:
            if (random.randrange(0, 2) == 0):
                action = ACTION.LEFT
            else:
                action = ACTION.RIGHT

        return action, (0, 0, 0)