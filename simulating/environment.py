"""
Environment module deals with storing and representing a
simulated world for the entities to move within.

Contains the Direction enum for dealing with orientation. 
"""

from enum import Enum
import math
import random

from simulating.action import Action


class Direction(Enum):
    """ Abstracts the concept of Direction within the world """

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def right(self):
        """ Returns the Direction clockwise to this one """
        if self == Direction.NORTH:
            return Direction.EAST
        if self == Direction.EAST:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.WEST
        return Direction.NORTH

    def left(self):
        """ Returns the Direction counterclockwise to this one """
        if self == Direction.NORTH:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.EAST
        return Direction.NORTH

    def to_string(self):
        """ Direction represented as a string """
        if self == Direction.NORTH:
            return "△"
        if self == Direction.EAST:
            return "▷"
        if self == Direction.SOUTH:
            return "▽"
        return "◁"


def get_random_direction():
    """ Returns a random Direction """
    return random.choice(list(Direction))


class MushroomNotFound(RuntimeError):
    """ Exception thrown when a call requires a mushroom but there isn't one """


class WorldFull(RuntimeError):
    """ Exception thrown when there isn't space left in the world to place something """


class Environment:
    """ Representation of the simulated world

    Allows for placing mushrooms and an entity within the world.
    Has methods for clearing spaces in the world,
    checking for adjacency, moving an entity, getting the closest
    mushroom to a cell and printing the world.

    Attributes:
        world: A hashmap reprsentation of the world according to positions of mushroom
        dim_x: The width of the 2D world
        dim_y: The height of the 2D world
        num_poisonous: The number of poisonous mushrooms
        num_edible: The number of edible mushrooms in the world
        entity_position: Position of the entity
        entity_direction: Direction the entity is currently facing
    """

    world = {}
    dim_x = 0
    dim_y = 0
    num_poisonous = 0
    num_edible = 0

    entity_position = (0, 0)
    entity_direction = Direction.NORTH

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

        self.dim_x = width
        self.dim_y = height
        self.num_poisonous = poisonous
        self.num_edible = edible
        self.reset()

    def reset(self):
        """ Reset the world
        
        Removes all remaining mushrooms and places the number of mushrooms needed randomly again.
        Doesn't reset the position of the entity.
        """

        self.world = {}
        for _ in range(self.num_edible):
            self.place_mushroom(make_edible())
        for _ in range(self.num_poisonous):
            self.place_mushroom(make_poisonous())

    # ----- Mushroom manipulation methods ----- #

    def place_mushroom(self, mushroom):
        """ Given a mushroom, place it at a random available position.
        
        Args:
            mushroom (int): Bit pattern for the mushroom to be placed.
        Raises:
            WorldFull: No space for the mushroom.
        """

        pos = self.random_available_position()
        self.world[pos] = mushroom

    def closest_mushroom(self, pos):
        """ Returns the distance to and distance from the closest mushroom in the world.
        
        Args:
            pos (int, int): Position searching from.
        Raises:
            MushroomNotFound: No mushrooms found.

        """

        if len(self.world) == 0:
            raise MushroomNotFound("No Mushrooms in World")
        dist = self.dim_x + self.dim_y + 1
        pos = (-1, -1)
        for (i, j) in self.world:
            # Use manhattan distance
            dist_to_mushroom = abs(pos[0] - i) + abs(pos[1] - j)
            if dist_to_mushroom < dist:
                dist = dist_to_mushroom
                pos = (i, j)
        return dist, pos

    def is_mushroom(self, pos):
        """ Returns whether or not there is a mushroom in a given position """
        return pos in self.world

    # ----- Entity manipulation methods ----- #

    def place_entity(self):
        """ Places an entity in a random available position in the world.

        Raises:
            WorldFull: No space for the entity.
        """

        self.entity_direction = get_random_direction()
        cell_occupied = True
        while cell_occupied:
            pos = self.random_available_position()
            if not pos in self.world:
                cell_occupied = False
                self.entity_position = pos

    def move_entity(self, action):
        """ Moves the entity in the world according to the Action taken.

        Args:
            Action: The Action to be taken.
        """

        if action == Action.FORWARDS:
            x = self.entity_position[0] + self.entity_direction.value[0]
            y = self.entity_position[1] + self.entity_direction.value[1]
            print(x, y)
            if self.within_bounds((x, y)):
                self.entity_position = (x, y)
        elif action == Action.LEFT:
            self.entity_direction = self.entity_direction.left()
        elif action == Action.RIGHT:
            self.entity_direction = self.entity_direction.right()

    def get_entity_position(self):
        """ Returns the position of the entity """
        return self.entity_position

    # ----- Utility methods ----- #

    def random_position(self):
        """ Return a random position within the world dimensions """
        return (random.randint(0, self.dim_x - 1),
                random.randint(0, self.dim_y - 1))

    def random_available_position(self):
        """ Return a random available position within the world dimensions
        
        Raises:
            WorldFull: No space for the entity.
        """

        if len(self.world) == self.dim_x * self.dim_y:
            raise WorldFull("No available spaces remaining in world")
        cell_occupied = True
        pos = (-1, -1)
        while cell_occupied:
            new_pos = random.randint(0, self.dim_x - 1), random.randint(
                0, self.dim_y - 1)
            if new_pos not in self.world:
                pos = new_pos
                cell_occupied = False
        return pos

    def within_bounds(self, pos):
        """ Checks if a position is within the world """
        x, y = pos
        return 0 <= x < self.dim_x and 0 <= y < self.dim_y

    def adjacent(self, pos_a, pos_b):
        """ Checks if two positions are adjacent to each other """

        x1, y1 = pos_a
        x2, y2 = pos_b
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

    def get_angle(self, pos_from, pos_to):
        """ Returns the angle from one position to another, from 0 to 1.

        The angle is measured clockwise where 0 is directly forwards.

        Args:
            pos_from: The starting position
            pos_to: The goal posision
        Returns:
            angle (float): The angle from 0 to 1.
        """

        x1, y1 = pos_from
        x2, y2 = pos_to
        if x1 == x2 and y1 == y2:
            return 0
        angle = -math.degrees(math.atan2(y1 - y2, x2 - x1))
        print(angle)
        if self.entity_direction == Direction.NORTH:
            angle += 90
        if self.entity_direction == Direction.WEST:
            angle += 180
        if self.entity_direction == Direction.SOUTH:
            angle -= 90
        print(angle % 360)
        return (angle % 360) / 360

    def get_cell(self, pos):
        """ Returns the value of the cell at position pos, 0 if empty"""

        return self.world.get(pos, 0)

    def clear_cell(self, pos):
        """ Clears the cell at a specified position """

        self.world.pop(pos, None)

    # ----- String conversion ----- #

    def __str__(self, distances=False):
        """ Converts the world to a 2D array string representation """

        out = []
        for j in range(self.dim_y):
            row = []
            for i in range(self.dim_x):
                c = cell_to_string(self.world.get((i, j), 0))
                if distances and not self.is_mushroom((i, j)):
                    c = str(self.closest_mushroom((i, j))[0])
                if (i, j) == self.entity_position:
                    c = self.entity_direction.to_string()
                row.append(c)
            out.append(' '.join(row))
        return '\n'.join(out)


# -- Various utility methods for mushrooms -- #


def cell_to_string(cell):
    """ Converts a cell to a string """

    if cell == 0:
        return '-'
    if is_poisonous(cell):
        return '🚫'
    if is_edible(cell):
        return '🍄'
    return '@'


def make_poisonous(i=random.randint(0, 9)):
    """ Generates a poisonous mushroom """

    return mutate(0b1111100000, i)


def make_edible(i=random.randint(0, 9)):
    """ Generates an edible mushroom """

    return mutate(0b0000011111, i)


def is_poisonous(cell):
    """ Checks if a mushroom is poisonous """

    lower_bits = cell & 0b111
    return not (lower_bits - 1) & lower_bits


def is_edible(cell):
    """ Checks if a mushroom is edible """

    return not is_poisonous(cell)


def mutate(mushroom, i):
    """ Randomly flips one bit in a mushroom bit string"""

    return mushroom ^ 1 << i
