from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Set

T = TypeVar('T')


class Group(ABC, Generic[T]):

    @abstractmethod
    def binary_operation(self, a: T, b: T) -> T:
        pass

    @abstractmethod
    def identity(self) -> T:
        pass

    @abstractmethod
    def inverse_of(self, a: T) -> T:
        pass

    def exponent(self, a: T, k: int) -> T:
        if k < 0:
            raise ValueError('k must be positive')
        return self.identity() if k == 0 else self.binary_operation(a, self.exponent(a, k - 1))


class BijectionGroup(Group[Callable[[T], T]]):

    def __init__(self, s: Set[T]):
        self.domain = s

    def binary_operation(self, f: Callable[[T], T], g: Callable[[T], T]) -> Callable[[T], T]:
        return lambda x: f(g(x))

    def identity(self) -> Callable[[T], T]:
        return lambda x: x

    def inverse_of(self, f: Callable[[T], T]) -> Callable[[T], T]:
        inverse = {f(x): x for x in self.domain}
        return lambda x: inverse[x]

    @staticmethod
    def bijection_group(domain: Set[T]) -> Group[Callable[[T], T]]:
        return BijectionGroup(domain)

    @staticmethod
    def bijections_of(s: Set[T]) -> set[Callable[[T], T]]:
        def permute(elements: list[T], arrangements: list[list[T]], bijection: list[T]):
            if len(bijection) == len(elements):
                arrangements.append(bijection)
            else:
                for e in elements:
                    if bijection.__contains__(e):
                        continue
                    bijection.append(e)
                    permute(elements, arrangements, bijection.copy())
                    bijection.pop()


        set_list = list(s)
        permutations = list()
        bijections = set()
        permute(set_list, permutations, [])

        for p in permutations:
            mapping = dict()
            for i in range(len(p)):
                mapping[set_list[i]] = p[i]
            bijections.add(lambda x, m=mapping: m[x])   #m=mapping ensures each function starts with a new, unaltered map

        return bijections


def print_bijections(bijections: Set[Callable[[T], T]], a_few: Set[T]) -> None:
    for a_bijection in bijections:
        for n in a_few:
            print(f"{n} --> {a_bijection(n)}", end="; ")
        print()


if __name__ == "__main__":
    three_ints: Set[int] = {1, 2, 3}
    test_bijections: Set[Callable[[int], int]] = BijectionGroup.bijections_of(three_ints)
    print_bijections(test_bijections, three_ints)


    g = BijectionGroup.bijection_group(three_ints)
    f1 = BijectionGroup.bijections_of(three_ints).pop()
    f2 = g.inverse_of(f1)
    identity = g.identity()

    for n in three_ints:
        print(f"{n} --> {f1(n)}", end="; ")
    print()

    for n in three_ints:
        print(f"{n} --> {f2(n)}", end="; ")
    print()

    for n in three_ints:
        print(f"{n} --> {g.binary_operation(f1, f2)(n)}", end="; ")
    print()

