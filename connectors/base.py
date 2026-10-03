from abc import ABC, abstractmethod


class Connector(ABC):
    source = None
    dataset = None

    def __init__(self, params=None):
        self.params = params or {}

    @abstractmethod
    def fetch(self):
        ...