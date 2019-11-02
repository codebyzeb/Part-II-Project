from enum import Enum
import environment
import random

ENERGY_POISON = -11
ENERGY_EDIBLE = 10

class ACTION(Enum):
    FORWARDS = 0b11
    LEFT = 0b10
    RIGHT = 0b01
    NOTHING = 0b00

class Entity:

    energy = 0

    def __init__(self, startEnergy=0):
        self.energy = startEnergy

    def eat(self, mushroom):
        if (environment.isEdible(mushroom)):
            self.energy += ENERGY_EDIBLE
        elif (environment.isPoisonous(mushroom)):
            self.energy += ENERGY_POISON

    def action(self, location, perception, listening):
        """ Given perceptual inputs, the entity generates an appropriate action.

        Args:
         location (float): Location of the nearest mushroom in angle from 0 to 1.
         perception: 10-bit properties of the adjacent mushroom
         listening: Audio inputs
        Returns:
         An action to be taken and the vocal response

        """

        # Temporary behaviour - just move towards the nearest mushroom

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
        

