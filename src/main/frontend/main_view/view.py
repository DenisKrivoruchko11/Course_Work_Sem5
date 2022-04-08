from json import JSONDecodeError
from typing import Optional, Callable

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from src.main.backend.operations.algebraic_operations import operation
from src.main.backend.models.canvas import Canvas
from src.main.backend.operations.set_theoretic_operations import union, intersection, substraction
from src.main.frontend.main_view.central_widget import configure_central_widget
from src.main.frontend.main_view.menu_bar import configure_menu_bar
from src.main.frontend.operation_result_view.view import OperationResultView
from src.main.backend.models.cyclogram import cyclogram_from_file, Cyclogram


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.left, self.right = Canvas(self), Canvas(self)
        self.stack, self.current_state = [(None, None)], 0

        self.setWindowTitle('Main')
        self.setMenuBar(configure_menu_bar(self))
        self.setCentralWidget(configure_central_widget(self, self.left, self.right))

    # position: -1: Left, 0: Both, 1: Right
    def set_cyclogram(self, position: int, left: Optional[Cyclogram] = None, right: Optional[Cyclogram] = None):
        self.current_state += 1
        if position <= 0:
            self.left.draw_cyclogram(left)
        if position >= 0:
            self.right.draw_cyclogram(right)
        self.stack = self.stack[:self.current_state] + [(self.left.cyclogram, self.right.cyclogram)]

    def open_button_click(self, position: int):
        path = QFileDialog.getOpenFileName(self, 'Choose a file')[0]
        if path:
            try:
                cyclogram = cyclogram_from_file(path)
                self.set_cyclogram(position, cyclogram, cyclogram)
            except FileNotFoundError:
                QMessageBox(QMessageBox.Warning, 'Error', 'File not found', parent=self).exec()
            except UnicodeDecodeError:
                QMessageBox(QMessageBox.Warning, 'Error', 'Not a text file', parent=self).exec()
            except JSONDecodeError:
                QMessageBox(QMessageBox.Warning, 'Error', 'Incorrect text file', parent=self).exec()
            except KeyError:
                QMessageBox(QMessageBox.Warning, 'Error', 'Incorrect json file', parent=self).exec()
            except TypeError:
                QMessageBox(QMessageBox.Warning, 'Error', 'Incorrect type of some fields', parent=self).exec()
            except ValueError:
                QMessageBox(QMessageBox.Warning, 'Error', 'Incorrect fields', parent=self).exec()
            except AttributeError as e:
                QMessageBox(QMessageBox.Warning, 'Error', str(e), parent=self).exec()

    def swap_button_click(self):
        self.set_cyclogram(0, self.right.cyclogram, self.left.cyclogram)

    def save_button_click(self, position: int):
        if position < 0 and self.left.cyclogram or position > 0 and self.right.cyclogram:
            path = QFileDialog.getSaveFileName(self, 'Input file name')[0]
            if path:
                (self.left.cyclogram if position < 0 else self.right.cyclogram).save_to_file(path)

    def close_button_click(self, position: int):
        self.set_cyclogram(position)

    def undo_button_click(self):
        if self.current_state > 0:
            self.current_state -= 1
            self.left.draw_cyclogram(self.stack[self.current_state][0])
            self.right.draw_cyclogram(self.stack[self.current_state][1])

    def redo_button_click(self):
        if self.current_state < len(self.stack) - 1:
            self.current_state += 1
            self.left.draw_cyclogram(self.stack[self.current_state][0])
            self.right.draw_cyclogram(self.stack[self.current_state][1])

    def execute_binary_operation(self, f: Callable):
        if self.left.cyclogram and self.right.cyclogram:
            try:
                OperationResultView(self, f(self.left.cyclogram, self.right.cyclogram)).show()
            except ValueError as e:
                QMessageBox(QMessageBox.Warning, 'Error', str(e), parent=self).exec()

    def union_button_click(self):
        self.execute_binary_operation(union)

    def intersection_button_click(self):
        self.execute_binary_operation(intersection)

    def substraction_button_click(self):
        self.execute_binary_operation(substraction)

    def operation_button_click(self):
        self.execute_binary_operation(operation)
