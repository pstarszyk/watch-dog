from abc import ABC


class Component(ABC):
    """
    Abstract class for all detector components.
    """

    def __init__(self):
        ...