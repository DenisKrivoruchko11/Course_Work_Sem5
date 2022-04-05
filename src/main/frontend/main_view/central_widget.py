from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMainWindow

from src.main.backend.models.canvas import Canvas


def configure_central_layout(parent: QWidget, left_canvas: Canvas, right_canvas: Canvas):
    layout = QHBoxLayout(parent)

    layout.addWidget(left_canvas)
    layout.addWidget(right_canvas)


def configure_central_widget(window: QMainWindow, left_canvas: Canvas, right_canvas: Canvas) -> QWidget:
    widget = QWidget(window)

    configure_central_layout(widget, left_canvas, right_canvas)

    return widget
