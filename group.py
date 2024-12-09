from abc import ABC, abstractmethod
from typing import TypeVar, Generic
T = TypeVar('T')

class Group(ABC, Generic[T]):
    @abstractmethod
    def binary_operation(self, f: T, g: T) -> T:
        pass;

    @abstractmethod
    def identity(self) -> T:
        pass

    @abstractmethod
    def inverse(self, f: T) -> T:
        pass

    def exponent(self, f: T, k: int) -> T:
        if k < 0:
            raise ValueError('k must be positive')
        return self.identity() if k == 0 else self.binary_operation(f, self.exponent(f, k-1))
