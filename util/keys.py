from enum import Enum


class Systems(Enum):
    Integro = 1
    Votetrust = 2
    Sybilframe = 3


class SF_Keys(Enum):
    Message = 1
    Potential = 2
    Belief = 3