from enum import Enum

class FitStrategy(Enum):
    MINIMIZE_WIDTH = 0
    MINIMIZE_HEIGHT = 1
    BALANCED = 2