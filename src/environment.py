"""
Environment module deals with storing and representing a simulated world for the entities to move within.

Contains the DIRECTION enum for dealing with orientation. 
"""

import random
from entity import ACTION
from enum import Enum
import math

class DIRECTION(Enum):
    """ Abstracts the concept of direction within the world """

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def right(self):
        """ Returns the direction clockwise to this one """
        if (self == DIRECTION.NORTH):
            return DIRECTION.EAST
        elif (self == DIRECTION.EAST):
            return DIRECTION.SOUTH
        elif (self == DIRECTION.SOUTH):
            return DIRECTION.WEST
        return DIRECTION.NORTH

    def left(self):
        """ Returns the direction counterclockwise to this one """
        if (self == DIRECTION.NORTH):
            return DIRECTION.WEST
        elif (self == DIRECTION.WEST):
            return DIRECTION.SOUTH
        elif (self == DIRECTION.SOUTH):
            return DIRECTION.EAST
        return DIRECTION.NORTH

    def toString(self):
        """ Direction represented as a string """
        if (self == DIRECTION.NORTH): return "△"
        elif (self == DIRECTION.EAST): return "▷"
        elif (self == DIRECTION.SOUTH): return "▽"
        return "◁"

def getRandomDirection():
    """ Returns a random direction """
    x = random.randrange(0, 4)
    if (x == 0): return DIRECTION.NORTH
    if (x == 1): return DIRECTION.EAST
    if (x == 2): return DIRECTION.SOUTH
    if (x == 3): return DIRECTION.WEST

class MushroomNotFound(RuntimeError):
    def __init__(self, arg):
      self.args = args

class WorldFull(RuntimeError):
   def __init__(self, arg):
      self.args = args

class Environment:
    """ Representation of the simulated world

    Allows for placing mushrooms and an entity within the world. Has methods for clearing spaces in the world,
    checking for adjacency, moving an entity, getting the closest mushroom to a cell and printing the world.

    Attributes:
        world: A hashmap reprsentation of the world according to positions of mushroom
        dimX: The width of the 2D world
        dimY: The height of the 2D world
        numPoisonous: The number of poisonous mushrooms
        numEdible: The number of edible mushrooms in the world
        entityPosition: Position of the entity
        entityDirection: Direction the entity is currently facing
    """

    world = {}
    dimX = 0
    dimY = 0
    numPoisonous = 0
    numEdible = 0

    entityPosition = (0, 0)
    entityDirection = DIRECTION.NORTH

    # ----- World Creation ----- #

    def __init__(self, width=20, height=20, poisonous=10, edible=10):
        """ Instantiate a new Environment object

        Args:
            width (int): The width of the world
            height (int): The height of the world
            poisonous (int): The number of poisonous mushrooms to place in the world
            edible (int): The number of edible mushrooms to place in the world
        Returns:
            env: A new Environment object
        Raises:
            WorldFull: World is full
        """

        self.dimX = width
        self.dimY = height
        self.numPoisonous = poisonous
        self.numEdible = edible
        self.reset()

    def reset(self):
        """ Reset the world
        
        Removes all remaining mushrooms and places the number of mushrooms needed randomly again.
        Doesn't reset the position of the entity.
        """

        self.world = {}
        for i in range(self.numEdible):
            self.placeMushroom(makeEdible())
        for i in range(self.numPoisonous):
            self.placeMushroom(makePoisonous())

    # ----- Mushroom manipulation methods ----- #

    def placeMushroom(self, mushroom):
        """ Given a mushroom, place it at a random available position.
        
        Args:
            mushroom (int): Bit pattern for the mushroom to be placed.
        Raises:
            WorldFull: No space for the mushroom.
        """

        pos = self.randomAvailablePosition()
        self.world[pos] = mushroom

    def closestMushroom(self, pos):
        """ Returns the distance to and distance from the closest mushroom in the world.
        
        Args:
            pos (int, int): Position searching from.
        Raises:
            MushroomNotFound: No mushrooms found.

        """

        if len(self.world) == 0: raise MushroomNotFound("No Mushrooms in World")
        x, y = pos
        dist = self.dimX + self.dimY + 1
        pos = (-1, -1)
        for (i, j) in self.world:
            # Use manhattan distance
            distToMushroom = abs(x - i) + abs(y - j)
            if distToMushroom < dist:
                dist = distToMushroom
                pos = (i, j)
        return dist, pos
                
    def isMushroom(self, pos):
        """ Returns whether or not there is a mushroom in a given position """
        return pos in self.world

    # ----- Entity manipulation methods ----- #

    def placeEntity(self):
        """ Places an entity in a random available position in the world.

        Raises:
            WorldFull: No space for the entity.
        """

        self.entityDirection = getRandomDirection()
        cellOccupied = True
        while cellOccupied:
            pos = self.randomAvailablePosition()
            if not pos in self.world:
                cellOccupied = False
                self.entityPosition = pos

    def moveEntity(self, action):
        """ Moves the entity in the world according to the action taken.

        Args:
            action: The action to be taken.
        Raises:
            WorldFull: No space for the entity.
        """

        if (action == ACTION.FORWARDS):
            x = self.entityPosition[0] + self.entityDirection.value[0]
            y = self.entityPosition[1] + self.entityDirection.value[1]
            print(x, y)
            if self.withinBounds((x, y)): self.entityPosition = (x, y)
        elif (action == ACTION.LEFT):
            self.entityDirection = self.entityDirection.left()
        elif (action == ACTION.RIGHT):
            self.entityDirection = self.entityDirection.right()

    def getEntityPosition(self):
        """ Returns the position of the entity """
        return self.entityPosition

    # ----- Utility methods ----- #

    def randomPosition(self):
        """ Return a random position within the world dimensions """
        return (random.randint(0, self.dimX-1), random.randint(0, self.dimY-1))

    def randomAvailablePosition(self):
        """ Return a random available position within the world dimensions """

        if len(self.world) == self.dimX * self.dimY: raise WorldFull("No available spaces remaining in world")
        cellOccupied = True
        pos = (-1, -1)
        while (cellOccupied):
            newPos = random.randint(0, self.dimX-1), random.randint(0, self.dimY-1)
            if not newPos in self.world: 
                pos = newPos
                cellOccupied = False
        return pos

    def withinBounds(self, pos):
        """ Checks if a position is within the world """
        x, y = pos
        return (x < self.dimX and x >= 0 and y < self.dimY and y >= 0)

    def adjacent(self, posA, posB):
        """ Checks if two positions are adjacent to each other """

        x1, y1 = posA
        x2, y2 = posB
        return (abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1)

    def getAngle(self, posFrom, posTo):
        """ Returns the angle from one position to another, from 0 to 1.

        The angle is measured clockwise where 0 is directly forwards.

        Args:
            posFrom: The starting position
            posTo: The goal posision
        Returns:
            angle (float): The angle from 0 to 1.
        """

        x1, y1 = posFrom
        x2, y2 = posTo
        angle = -math.degrees(math.atan2(y1-y2, x2-x1))
        print(angle)
        if (self.entityDirection == DIRECTION.NORTH): angle+=90
        if (self.entityDirection == DIRECTION.WEST): angle+=180
        if (self.entityDirection == DIRECTION.SOUTH): angle-=90
        print(angle % 360)
        return (angle % 360)/360

    def getCell(self, pos):
        """ Returns the value of the cell at position pos, 0 if empty"""

        return self.world.get(pos, 0)
    
    def clearCell(self, pos):
        """ Clears the cell at a specified position """

        self.world.pop(pos, None)

    # ----- String conversion ----- #

    def __str__(self, distances=False):
        """ Converts the world to a 2D array string representation """

        out = []
        for j in range(self.dimY):
            row = []
            for i in range(self.dimX):
                c = cellToString(self.world.get((i, j), 0))
                if distances and not self.isMushroom((i, j)):
                    c = str(self.closestMushroom(i, j)[0])
                if ((i, j) == self.entityPosition):
                    c = self.entityDirection.toString()
                row.append(c)
            out.append(' '.join(row))
        return '\n'.join(out)

# -- Various utility methods for mushrooms -- #

def cellToString(cell):
    """ Converts a cell to a string """

    if (cell == 0): return '-'
    if (isPoisonous(cell)): return '🚫'
    if (isEdible(cell)): return '🍄'
    return '@'

def makePoisonous():
    """ Generates a poisonous mushroom """

    return mutate(0b1111100000)

def makeEdible():
    """ Generates an edible mushroom """

    return mutate(0b0000011111)

def isPoisonous(cell):
    """ Checks if a mushroom is poisonous """

    lowerBits = cell & 0b111
    return not ((lowerBits - 1) & lowerBits)

def isEdible(cell):
    """ Checks if a mushroom is edible """

    return not(isPoisonous(cell))

def mutate(mushroom):
    """ Randomly flips one bit in a mushroom bit string"""

    i = random.randint(0, 9)
    return mushroom ^ 1 << i


