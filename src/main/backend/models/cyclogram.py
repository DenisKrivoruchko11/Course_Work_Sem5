import json
from typing import List

import portion


class Cyclogram(object):
    def __init__(self, name: str, set1_elements: List[str], set2_elements: List[str],
                 start_time: float, end_time: float, intervals: List[List[portion.Interval]]):
        if len(set1_elements) != len(set(set1_elements)) or len(set2_elements) != len(set(set2_elements)):
            raise AttributeError('Set contain equal elements')
        if start_time >= end_time:
            raise AttributeError('Start time greater or equal than end time')
        if len(intervals) != len(set1_elements):
            raise AttributeError('Incorrect intervals matrix')

        self.name = name
        self.set1_elements, self.set2_elements = set1_elements, set2_elements
        self.start_time, self.end_time = start_time, end_time

        self.intervals = []
        for row in intervals:
            if len(row) != len(set2_elements):
                raise AttributeError('Incorrect intervals matrix')
            else:
                self.intervals.append([interval & portion.closed(start_time, end_time) for interval in row])

    def save_to_file(self, path: str):
        data = self.__dict__.copy()
        data['intervals'] = [[portion.to_data(interval) for interval in row] for row in data['intervals']]
        with open(path, 'w') as f:
            json.dump(data, f)


def cyclogram_from_file(path: str) -> Cyclogram:
    with open(path, 'r') as f:
        data = json.load(f)
    data['intervals'] = [[portion.from_data(interval) for interval in row] for row in data['intervals']]
    return Cyclogram(data['name'], data['set1_elements'], data['set2_elements'],
                     data['start_time'], data['end_time'], data['intervals'])
