"""
Environment module deals with storing and representing a
simulated world for the entities to move within.

Contains the Direction enum for dealing with orientation. 
"""

from enum import Enum
import math
import random

from simulating.action import Action

# Used for indexing positions
X = 0
Y = 1


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
        world: A dictionary representation of the world according to positions of mushroom
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

    def __init__(self, width=20, height=20, poisonous=10, edible=10, debug=False):
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
        self.debug = debug
        self.reset()

    def reset(self):
        """ Reset the world
        
        Removes all remaining mushrooms and places the number of mushrooms needed randomly again.
        Doesn't reset the position of the entity.
        """

        self.world = {}
        if self.debug:
            self.generate_fixed_world()
        else:
            for _ in range(self.num_edible):
                self.place_mushroom(make_edible())
            for _ in range(self.num_poisonous):
                self.place_mushroom(make_poisonous())

    def generate_fixed_world(self):
        """ Generates a fixed world deterministically
        for debugging purposes
        """

        for i, (x, y) in enumerate([(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]):
            self.world[(x + 5, y + 5)] = make_edible(i)
            self.world[(x + 15, y + 5)] = make_poisonous(i)
            self.world[(x + 5, y + 15)] = make_edible(i + 5)
            self.world[(x + 15, y + 15)] = make_poisonous(i + 5)

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
        """ Returns the position to the closest mushroom in the world.
        
        Args:
            pos (int, int): Position searching from.
        Raises:
            MushroomNotFound: No mushrooms found.

        """

        if len(self.world) == 0:
            raise MushroomNotFound("No Mushrooms in World")
        dist = self.dim_x + self.dim_y + 1
        mush_pos = (-1, -1)
        for (i, j) in self.world:
            # Use manhattan distance
            dist_to_mushroom = abs(pos[X] - i) + abs(pos[Y] - j)
            if dist_to_mushroom < dist:
                dist = dist_to_mushroom
                mush_pos = (i, j)

        return mush_pos

    def is_mushroom(self, pos):
        """ Returns whether or not there is a mushroom in a given position """
        return pos in self.world

    # ----- Entity manipulation methods ----- #

    def place_entity(self):
        """ Places an entity in a random available position in the world.

        Raises:
            WorldFull: No space for the entity.
        """
        if self.debug:
            self.entity_direction = Direction.NORTH
            self.entity_position = (10, 10)
        else:
            self.entity_direction = get_random_direction()
            pos = self.random_available_position()
            self.entity_position = pos

    def move_entity(self, action):
        """ Moves the entity in the world according to the Action taken.

        Args:
            Action: The Action to be taken.
        """

        if action == Action.FORWARDS:
            x = self.entity_position[X] + self.entity_direction.value[X]
            y = self.entity_position[Y] + self.entity_direction.value[Y]
            if self.within_bounds((x, y)):
                self.entity_position = (x, y)
        elif action == Action.LEFT:
            self.entity_direction = self.entity_direction.left()
        elif action == Action.RIGHT:
            self.entity_direction = self.entity_direction.right()

    def get_entity_position(self):
        """ Returns the position of the entity """
        return self.entity_position

    def entity_facing_out(self):
        """ Returns true if the entity is at the edge of the world and facing out
        """
        if self.entity_direction == Direction.NORTH and self.entity_position[Y] == 0:
            return True
        if self.entity_direction == Direction.EAST and self.entity_position[X] == self.dim_x - 1:
            return True
        if self.entity_direction == Direction.SOUTH and self.entity_position[Y] == self.dim_y - 1:
            return True
        if self.entity_direction == Direction.WEST and self.entity_position[X] == 0:
            return True
        return False

    def get_entity_angle_to_position(self, pos_to):
        """ Returns the angle from the entity to a position, from 0 to 1.

        The angle is measured clockwise where 0 is directly forwards.

        Args:
            pos_to: The goal posision
        Returns:
            angle (float): The angle from 0 to 1.
        """

        return self.get_angle(self.entity_position, pos_to, self.entity_direction)

    # ----- Utility methods ----- #

    def random_position(self):
        """ Return a random position within the world dimensions """
        return (random.randint(0, self.dim_x - 1), random.randint(0, self.dim_y - 1))

    def random_available_position(self):
        """ Return a random available position within the world dimensions
        
        Raises:
            WorldFull: No space available
        """

        if len(self.world) == self.dim_x * self.dim_y:
            raise WorldFull("No available spaces remaining in world")
        cell_occupied = True
        pos = (-1, -1)
        while cell_occupied:
            new_pos = random.randint(0, self.dim_x - 1), random.randint(0, self.dim_y - 1)
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

    def get_angle(self, pos_from, pos_to, direction):
        """ Returns the angle from the entity to a position, from 0 to 1.

        The angle is measured clockwise where 0 is directly forwards.

        Args:
            pos_to: The goal posision
        Returns:
            angle (float): The angle from 0 to 1.
        """

        x1, y1 = pos_from
        x2, y2 = pos_to
        if x1 == x2 and y1 == y2:
            return 0
        angle = -math.degrees(math.atan2(y1 - y2, x2 - x1))
        if direction == Direction.NORTH:
            angle += 90
        if direction == Direction.WEST:
            angle += 180
        if direction == Direction.SOUTH:
            angle -= 90
        return (angle % 360) / 360

    def get_cell(self, pos):
        """ Returns the value of the cell at position pos, 0 if empty"""

        return self.world.get(pos, 0)

    def clear_cell(self, pos):
        """ Clears the cell at a specified position """

        self.world.pop(pos, None)

    # ----- String conversion ----- #

    def __str__(self):
        """ Converts the world to a 2D array string representation """

        out = []
        for j in range(self.dim_y):
            row = []
            for i in range(self.dim_x):
                c = cell_to_string(self.world.get((i, j), 0))
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


def make_poisonous(i=-1):
    """ Generates a poisonous mushroom """

    return mutate(0b0000011111, i if i >= 0 else random.randint(0, 9))


def make_edible(i=-1):
    """ Generates an edible mushroom """

    return mutate(0b1111100000, i if i >= 0 else random.randint(0, 9))


def is_edible(cell):
    """ Checks if a mushroom is edible """

    lower_bits = cell & 0b111
    return not (lower_bits - 1) & lower_bits


def is_poisonous(cell):
    """ Checks if a mushroom is poisonous """

    return not is_edible(cell)


def mutate(mushroom, i):
    """ Randomly flips one bit in a mushroom bit string"""

    return mushroom ^ 1 << i
