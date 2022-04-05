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
            x_ticks, y_ticks, y_ticks_labels = [], [], []
            h = vertical_space_height
            for row, column in product(range(rows_count), range(columns_count)):
                y_ticks.append(h + rectangle_height / 2)
                y_ticks_labels.append(f'{cyclogram.set1_elements[-row - 1]}*{cyclogram.set2_elements[-column - 1]}')
                if not cyclogram.intervals[row][column].empty:
                    for interval in list(cyclogram.intervals[row][column]):
                        self.ax.add_patch(Rectangle((interval.lower, h), interval.upper - interval.lower,
                                                    rectangle_height))
                        self.ax.axvline(x=interval.lower)
                        x_ticks.append(interval.lower)
                        self.ax.axvline(x=interval.upper)
                        x_ticks.append(interval.upper)
                h += vertical_space_height + rectangle_height

            self.ax.set_title(cyclogram.name)
            self.ax.set_xticks(x_ticks)
            self.ax.set_yticks(y_ticks)
            self.ax.set_yticklabels(y_ticks_labels if rows_count * columns_count < 30 else ['' for _ in y_ticks])
            self.ax.set_ylim((0, h))

        self.cyclogram = cyclogram
        self.draw()

    def set_cyclogram_name(self, name: str):
        self.cyclogram.name = name
        self.ax.set_title(name)
        self.draw()
