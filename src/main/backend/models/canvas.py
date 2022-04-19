from itertools import product
from typing import Optional

from PyQt5.QtWidgets import QMainWindow
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle

from src.main.backend.models.cyclogram import Cyclogram


class Canvas(FigureCanvas):
    def __init__(self, parent: QMainWindow):
        fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Relation')
        self.cyclogram = None
        super().__init__(fig)
        self.setParent(parent)

    def draw_cyclogram(self, cyclogram: Optional[Cyclogram]):
        self.ax.clear()
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Relation')

        if cyclogram:
            rectangle_height, vertical_space_height = 0.5, 0.5
            rows_count, columns_count = len(cyclogram.set1_elements), len(cyclogram.set2_elements)
            x_ticks, y_ticks, y_ticks_labels = {cyclogram.start_time, cyclogram.end_time}, [], []
            h = vertical_space_height
            for row, column in product(range(rows_count - 1, -1, -1), range(columns_count - 1, -1, -1)):
                y_ticks.append(h + rectangle_height / 2)
                y_ticks_labels.append(f'<{cyclogram.set1_elements[row]}, {cyclogram.set2_elements[column]}>')
                if not cyclogram.intervals[row][column].empty:
                    for interval in list(cyclogram.intervals[row][column]):
                        self.ax.add_patch(Rectangle((interval.lower, h), interval.upper - interval.lower,
                                                    rectangle_height))
                        self.ax.axvline(x=interval.lower)
                        x_ticks.add(interval.lower)
                        self.ax.axvline(x=interval.upper)
                        x_ticks.add(interval.upper)
                h += vertical_space_height + rectangle_height
            self.ax.axvline(x=cyclogram.start_time)
            x_ticks.add(cyclogram.start_time)
            self.ax.axvline(x=cyclogram.end_time)
            x_ticks.add(cyclogram.end_time)

            self.ax.set_title(cyclogram.name)
            self.ax.set_xticks(list(x_ticks))
            self.ax.set_yticks(y_ticks)
            self.ax.set_yticklabels(y_ticks_labels if rows_count * columns_count < 30 else ['' for _ in y_ticks])
            self.ax.set_ylim((0, h))
            self.ax.annotate("", (1, 0), (-2, 0), 'axes fraction', 'offset points', {'arrowstyle': 'fancy'})
            self.ax.annotate("", (0, 1), (0, -2), 'axes fraction', 'offset points', {'arrowstyle': 'fancy'})

        self.cyclogram = cyclogram
        self.draw()

    def set_cyclogram_name(self, name: str):
        self.cyclogram.name = name
        self.ax.set_title(name)
        self.draw()
