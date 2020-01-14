"""
Options module describes the Options class used to configure simulations;
the simulation options are neatly packaged into this object.

"""

from enum import Enum


class Language(Enum):
    """ Represent possible types of languages """

    NONE = 0
    EXTERNAL = 1
    EVOLVED = 2


class Options:
    """ Used to configure a simulation.

    Attributes:
    """

    language_type = Language.NONE
    interactive = False
    record_language = False
    foldername = "temporary"
    threading = False

    def __init__(self,
                 language_type,
                 interactive,
                 record_language,
                 foldername,
                 threading=True):
        self.language_type = language_type
        self.interactive = interactive
        self.record_language = record_language
        self.foldername = foldername
        self.threading = threading

    def isNone(self):
        """ Returns true if the language type is none """
        return self.language_type == Language.NONE

    def isExternal(self):
        """ Returns true if the language type is external """
        return self.language_type == Language.EXTERNAL

    def isEvolved(self):
        """ Returns true if the language type is evolved """
        return self.language_type == Language.EVOLVED
