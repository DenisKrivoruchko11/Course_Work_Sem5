from typing import Callable

from portion import Interval

from src.main.backend.models.cyclogram import Cyclogram


def set_theoretic_operation(x: Cyclogram, y: Cyclogram, name: str, f: Callable) -> Cyclogram:
    if x.start_time != y.start_time or x.end_time != y.end_time:
        raise ValueError('Cyclograms have different time intervals')
    if x.set1_elements != y.set1_elements or x.set2_elements != y.set2_elements:
        raise ValueError('Cyclograms have different sets of elements')

    return Cyclogram(name, x.set1_elements, x.set2_elements, x.start_time, x.end_time,
                     [[f(x.intervals[row][column], y.intervals[row][column]) for column in range(len(x.set2_elements))]
                      for row in range(len(x.set1_elements))])


def union(x: Cyclogram, y: Cyclogram) -> Cyclogram:
    return set_theoretic_operation(x, y, f'{x.name} | {y.name}', Interval.union)


def intersection(x: Cyclogram, y: Cyclogram) -> Cyclogram:
    return set_theoretic_operation(x, y, f'{x.name} & {y.name}', Interval.intersection)


def substraction(x: Cyclogram, y: Cyclogram) -> Cyclogram:
    return set_theoretic_operation(x, y, f'{x.name} \\ {y.name}', Interval.difference)
