"""
This module runs all the tests for the Environment class
"""

import pytest

from simulating import environment
from simulating.action import Action
from simulating.environment import Direction
from simulating.environment import Environment
from simulating.environment import MushroomNotFound
from simulating.environment import WorldFull


def test_init_world_size():
    """
    This tests that the initial energy is set in the constructor
    """

    env = Environment(30, 40, 20, 20)
    assert (env.dim_x == 30 and env.dim_y == 40 and env.num_poisonous == 20
            and env.num_edible == 20)


def test_init_mushrooms_placed():
    """
    Ensure that the initial world is has the right number of mushrooms
    """

    env = Environment(10, 10, 10, 10)
    assert len(env.world) == env.num_edible + env.num_poisonous


def test_init_world_full():
    """
    Raises WorldFull if too many mushrooms placed
    """

    with pytest.raises(WorldFull):
        Environment(2, 2, 10, 10)


def test_reset_mushrooms_placed():
    """
    Ensure that a reset world is empty
    """

    env = Environment(10, 10, 10, 10)
    env.place_mushroom(0b111110000)
    env.reset()
    assert len(env.world) == env.num_edible + env.num_poisonous


def test_place_mushroom_bigger_world():
    """
    Check that the world is bigger
    """

    env = Environment(10, 10, 10, 10)
    world_size = len(env.world)
    env.place_mushroom(0b1111100000)
    assert len(env.world) == world_size + 1


def test_place_mushroom_world_full():
    """
    Check that the WorldFull is raised if world is full
    and placing a mushroom
    """

    env = Environment(2, 2, 2, 2)
    with pytest.raises(WorldFull):
        env.place_mushroom(0b0000011111)


def test_closest_mushroom_no_mushrooms():
    """
    Check that an exception is thrown if no mushrooms are in the world
    """

    env = Environment(10, 10, 0, 0)
    with pytest.raises(MushroomNotFound):
        env.closest_mushroom((5, 5))


def test_closest_mushroom_returns_in_bounds():
    """
    Check that the closest mushroom is correctly returned
    """

    env = Environment(10, 10, 1, 1)
    dist, pos = env.closest_mushroom((5, 5))
    assert dist < env.dim_x + env.dim_y
    assert env.within_bounds(pos)


def test_is_mushroom():
    """
    Check that the world returns whether or not a mushroom is in a position
    """

    env = Environment(10, 10, 0, 0)
    env.world[(1, 1)] = 0b1111100000
    assert env.is_mushroom((1, 1))
    assert not env.is_mushroom((2, 2))


def test_place_entity_world_full():
    """
    Tests that an exception is thrown if the world is full
    """

    env = Environment(2, 2, 2, 2)
    with pytest.raises(WorldFull):
        env.place_entity()


def test_move_entity_forwards():
    """
    Tests that moving the entity changes its position
    """

    env = Environment(3, 3, 0, 0)
    env.entity_direction = Direction.SOUTH
    env.entity_position = (0, 0)
    env.move_entity(Action.FORWARDS)
    assert env.entity_position == (0, 1)
    assert env.entity_direction == Direction.SOUTH
    env.move_entity(Action.FORWARDS)
    assert env.entity_position == (0, 2)
    assert env.entity_direction == Direction.SOUTH


def test_move_entity_right():
    """
    Tests that moving the entity changes its position
    """

    env = Environment(3, 3, 0, 0)
    env.entity_direction = Direction.SOUTH
    env.entity_position = (0, 1)
    env.move_entity(Action.RIGHT)
    assert env.entity_direction == Direction.WEST
    assert env.entity_position == (0, 1)


def test_move_entity_left():
    """
    Tests that moving the entity changes its position
    """

    env = Environment(3, 3, 0, 0)
    env.entity_direction = Direction.NORTH
    env.entity_position = (0, 1)
    env.move_entity(Action.LEFT)
    assert env.entity_direction == Direction.WEST
    assert env.entity_position == (0, 1)


def test_move_entity_nothing():
    """
    Tests that moving the entity changes its position
    """

    env = Environment(3, 3, 0, 0)
    env.entity_direction = Direction.SOUTH
    env.entity_position = (0, 1)
    env.move_entity(Action.NOTHING)
    assert env.entity_direction == Direction.SOUTH
    assert env.entity_position == (0, 1)


def test_get_entity_position():
    """
    Tests that position is correctly retrieved
    """

    env = Environment(3, 3, 0, 0)
    env.entity_position = (0, 1)
    assert env.get_entity_position() == (0, 1)


def test_random_available_position():
    """
    Check that the closest mushroom is correctly returned
    """

    env = Environment(10, 10, 40, 40)
    for _ in range(10):
        assert env.get_cell(env.random_available_position()) == 0


def test_random_available_position_world_full():
    """
    Check that an exception is thrown when the world is full
    """

    env = Environment(4, 4, 8, 8)
    with pytest.raises(WorldFull):
        env.random_available_position()


def test_within_bounds_true():
    """
    Tests that within bounds returns true when position in the grid
    """

    env = Environment(10, 10, 0, 0)
    assert env.within_bounds((5, 5))


def test_within_bounds_false():
    """
    Tests that within bounds returns true when position in the grid
    """

    env = Environment(10, 10, 0, 0)
    assert not env.within_bounds((1, -1))
    assert not env.within_bounds((10, 4))
    assert not env.within_bounds((-5, 4))
    assert not env.within_bounds((5, 14))


def test_adjacent_true():
    """
    Tests the adjacent function.
    """

    env = Environment(5, 5, 4, 4)
    assert env.adjacent((2, 2), (3, 3))
    assert env.adjacent((2, 2), (2, 1))
    assert env.adjacent((4, 4), (4, 4))


def test_entity_facing_out_true():
    """
    Tests that entity_facing_out returns true at each edge
    """

    env = Environment(5, 5, 0, 0)
    env.entity_direction = Direction.NORTH
    env.entity_position = (3, 0)
    assert env.entity_facing_out()
    env.entity_direction = Direction.EAST
    env.entity_position = (4, 2)
    assert env.entity_facing_out()
    env.entity_direction = Direction.SOUTH
    env.entity_position = (3, 4)
    assert env.entity_facing_out()
    env.entity_direction = Direction.WEST
    env.entity_position = (0, 3)
    assert env.entity_facing_out()


def test_entity_facing_out_false():
    """
    Tests that entity_facing_out returns true at each edge
    """

    env = Environment(5, 5, 0, 0)
    env.entity_direction = Direction.NORTH
    env.entity_position = (2, 3)
    assert not env.entity_facing_out()
    env.entity_direction = Direction.EAST
    env.entity_position = (3, 0)
    assert not env.entity_facing_out()
    env.entity_direction = Direction.SOUTH
    env.entity_position = (0, 0)
    assert not env.entity_facing_out()
    env.entity_direction = Direction.WEST
    env.entity_position = (4, 0)
    assert not env.entity_facing_out()


def test_get_angle():
    """
    Tests the angle function.
    """

    env = Environment(3, 3, 0, 0)
    env.entity_direction = Direction.NORTH
    assert env.get_angle((1, 1), (1, 1)) == 0
    assert env.get_angle((1, 1), (1, 0)) == 0
    assert env.get_angle((1, 1), (2, 0)) == 0.125
    assert env.get_angle((1, 1), (2, 1)) == 0.25
    assert env.get_angle((1, 1), (2, 2)) == 0.375
    assert env.get_angle((1, 1), (1, 2)) == 0.5
    assert env.get_angle((1, 1), (0, 2)) == 0.625
    assert env.get_angle((1, 1), (0, 1)) == 0.75
    assert env.get_angle((1, 1), (0, 0)) == 0.875


def test_get_cell_empty():
    """
    Test that 0 is returned if cell empty
    """

    env = Environment(1, 1, 0, 0)
    assert env.get_cell((0, 0)) == 0


def test_get_cell_edible():
    """
    Test that the mushroom is returned if cell occupied
    """

    env = Environment(1, 1, 0, 1)
    assert environment.is_edible(env.get_cell((0, 0)))


def test_clear_cell():
    """
    Test that a cell is cleared
    """

    env = Environment(1, 1, 1, 0)
    env.clear_cell((0, 0))
    assert env.get_cell((0, 0)) == 0
    assert len(env.world) == 0


def test_poisonous_true():
    """
    Test that poisonous mushrooms are poisonous
    """

    for i in range(10):
        assert environment.is_poisonous(environment.make_poisonous(i))


def test_edible_true():
    """
    Test that edible mushrooms are edible
    """

    for i in range(10):
        assert environment.is_edible(environment.make_edible(i))


def test_poisonous_false():
    """
    Test that edible mushrooms are not poisonous
    """

    for i in range(10):
        assert not environment.is_poisonous(environment.make_edible(i))


def test_edible_false():
    """
    Test that poisonous mushrooms are not edible
    """

    for i in range(10):
        assert not environment.is_edible(environment.make_poisonous(i))
