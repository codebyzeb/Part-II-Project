import random
from entity import ACTION
from enum import Enum
import math

class DIRECTION(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def right(self):
        if (self == DIRECTION.NORTH):
            return DIRECTION.EAST
        elif (self == DIRECTION.EAST):
            return DIRECTION.SOUTH
        elif (self == DIRECTION.SOUTH):
            return DIRECTION.WEST
        return DIRECTION.NORTH

    def left(self):
        if (self == DIRECTION.NORTH):
            return DIRECTION.WEST
        elif (self == DIRECTION.WEST):
            return DIRECTION.SOUTH
        elif (self == DIRECTION.SOUTH):
            return DIRECTION.EAST
        return DIRECTION.NORTH

    def toString(self):
        if (self == DIRECTION.NORTH): return "△"
        elif (self == DIRECTION.EAST): return "▷"
        elif (self == DIRECTION.SOUTH): return "▽"
        return "◁"

    def random(self):
        x = random.randrange(0, 4)
        if (x == 0): return DIRECTION.NORTH
        if (x == 1): return DIRECTION.EAST
        if (x == 2): return DIRECTION.SOUTH
        if (x == 3): return DIRECTION.WEST

class Environment:

    # 2D array representation
    # TODO: Consider list representation for efficiency given sparse world 
    world = []
    dimX = 0
    dimY = 0
    numPoisonous = 0
    numEdible = 0

    entityPosition = (0, 0)
    entityDirection = DIRECTION.NORTH

    def __init__(self, width=20, height=20, poisonous=10, edible=10):
        # Create the world
        self.dimX = width
        self.dimY = height
        self.numPoisonous = poisonous
        self.numEdible = edible
        self.reset()

    def reset(self):
        self.world = [[0] * self.dimY for i in range(self.dimX)] 
        # Place edible and poisonous mushrooms
        for i in range(self.numEdible):
            self.placeMushroom(makeEdible())
        for i in range(self.numPoisonous):
            self.placeMushroom(makePoisonous())

    def placeMushroom(self, mushroom):
        # Loop until cell found to place mushroom
        cellOccupied = True
        while cellOccupied:
            (x, y) = self.randomPosition()
            if self.world[x][y] == 0:
                cellOccupied = False
                self.world[x][y] = mushroom

    def randomPosition(self):
        return (random.randint(0, self.dimX-1), random.randint(0, self.dimY-1))

    def placeEntity(self):
        self.entityDirection = DIRECTION.NORTH.random()
        cellOccupied = True
        while cellOccupied:
            (x, y) = self.randomPosition()
            if self.world[x][y] == 0:
                cellOccupied = False
                self.entityPosition = (x, y)

    def withinBounds(self, x, y):
        return (x < self.dimX and x >= 0 and y < self.dimY and y >= 0)

    def moveEntity(self, action):
        if (action == ACTION.FORWARDS):
            x = self.entityPosition[0] + self.entityDirection.value[0]
            y = self.entityPosition[1] + self.entityDirection.value[1]
            print(x, y)
            if self.withinBounds(x, y): self.entityPosition = (x, y)
        elif (action == ACTION.LEFT):
            self.entityDirection = self.entityDirection.left()
        elif (action == ACTION.RIGHT):
            self.entityDirection = self.entityDirection.right()

    def getEntityPosition(self):
        return self.entityPosition

    def adjacent(self, posA, posB):
        x1, y1 = posA
        x2, y2 = posB
        return (abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1)

    def getAngle(self, posFrom, posTo):
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
        x, y = pos
        return self.world[x][y]

    def clearCell(self, pos):
        x, y = pos
        self.world[x][y] = 0

    #TODO: Make exception for mushroom not found

    def closestMushroom(self, pos):
        x, y = pos
        dist = self.dimX + self.dimY + 1
        pos = (-1, -1)
        for i in range(self.dimX):
            for j in range(self.dimY):
                if self.isMushroom((i, j)):
                    # Use manhattan distance
                    distToMushroom = abs(x - i) + abs(y - j)
                    if distToMushroom < dist:
                        dist = distToMushroom
                        pos = (i, j)
        return dist, pos
                
    def isMushroom(self, pos):
        x, y = pos
        return (self.world[x][y] != 0)

    def __str__(self, distances=False):
        out = []
        for j in range(self.dimY):
            row = []
            for i in range(self.dimX):
                c = cellToString(self.world[i][j])
                if distances and not self.isMushroom((i, j)):
                    c = str(self.closestMushroom(i, j)[0])
                if ((i, j) == self.entityPosition):
                    c = self.entityDirection.toString()
                row.append(c)
            out.append(' '.join(row))
        return '\n'.join(out)

# -- Various utility methods for mushrooms -- #

def cellToString(cell):
    if (cell == 0): return '-'
    if (isPoisonous(cell)): return '🚫'
    if (isEdible(cell)): return '🍄'
    return '@'

def makePoisonous():
    return mutate(0b1111100000)

def makeEdible():
    return mutate(0b0000011111)

def isPoisonous(cell):
    lowerBits = cell & 0b111
    return not ((lowerBits - 1) & lowerBits)

def isEdible(cell):
    return not(isPoisonous(cell))

def mutate(mushroom):
    i = random.randint(0, 9)
    return mushroom ^ 1 << i