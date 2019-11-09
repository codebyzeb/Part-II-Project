"""
Simple module just to store the Action enum.
"""

from enum import Enum


class Action(Enum):
    """ Representation of an Action
    """

    FORWARDS = 0b11
    LEFT = 0b10
    RIGHT = 0b01
    NOTHING = 0b00
