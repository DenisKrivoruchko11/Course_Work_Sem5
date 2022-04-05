from typing import Callable, Union

from PyQt5.QtWidgets import QMenu, QAction, QMainWindow, QMenuBar


def configure_action(window: QMainWindow, text: str, f: Callable, shortcut=None) -> QAction:
    action = QAction(text, window)

    if shortcut is not None:
        action.setShortcut(shortcut)
    action.triggered.connect(f)

    return action


def configure_choose_menu_action(window: QMainWindow, parent: Union[QMenu, QMenuBar],
                                 title: str, f: Callable) -> QAction:
    menu = QMenu(title, parent)

    menu.addActions([configure_action(window, 'Left', lambda: f(-1)),
                     configure_action(window, 'Right', lambda: f(1))])

    return menu.menuAction()
