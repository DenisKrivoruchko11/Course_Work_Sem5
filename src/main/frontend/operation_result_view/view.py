from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from src.main.frontend.operation_result_view.menu_bar import configure_menu_bar
from src.main.backend.models.canvas import Canvas
from src.main.backend.models.cyclogram import Cyclogram


class OperationResultView(QMainWindow):
    def __init__(self, previous_view: QMainWindow, cyclogram: Cyclogram):
        super().__init__()

        self.previous_view = previous_view
        self.canvas = Canvas(self)
        self.canvas.draw_cyclogram(cyclogram)

        self.setWindowTitle('Operation result')
        self.setCentralWidget(self.canvas)
        self.setMenuBar(configure_menu_bar(self))

    def set_name_button_click(self):
        name, ok_clicked = QInputDialog.getText(self, '', 'Input cyclogram name')
        if ok_clicked:
            self.canvas.set_cyclogram_name(name)

    def save_button_click(self):
        path = QFileDialog.getSaveFileName(self, 'Input file name')[0]
        if path:
            self.canvas.cyclogram.save_to_file(path)

    def open_button_click(self, position: int):
        self.previous_view.set_cyclogram(position, self.canvas.cyclogram, self.canvas.cyclogram)
        self.hide()
