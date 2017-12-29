from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    def find_all(self):
        return

    @abstractmethod
    def find_by_id(self):
        return

    @abstractmethod
    def create(self):
        return

    @abstractmethod
    def update(self):
        return

    @abstractmethod
    def delete(self):
        return
