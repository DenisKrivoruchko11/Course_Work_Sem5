from PyQt5.QtWidgets import QMenu, QMenuBar, QAction, QMainWindow

from src.main.frontend.common import configure_action, configure_choose_menu_action


def configure_edit_menu_action(window: QMainWindow, parent: QMenu) -> QAction:
    menu = QMenu('Edit', parent)

    menu.addActions([configure_action(window, 'Undo', window.undo_button_click, 'Ctrl+Z'),
                     configure_action(window, 'Redo', window.redo_button_click, 'Ctrl+Shift+Z'),
                     configure_action(window, 'Swap cyclograms', window.swap_button_click)])

    return menu.menuAction()


def configure_file_menu_action(window: QMainWindow, parent: QMenuBar) -> QAction:
    menu = QMenu('File', parent)

    menu.addActions([configure_choose_menu_action(window, menu, 'Open', window.open_button_click),
                     configure_edit_menu_action(window, menu),
                     configure_choose_menu_action(window, menu, 'Save', window.save_button_click),
                     configure_choose_menu_action(window, menu, 'Close', window.close_button_click)])

    return menu.menuAction()


def configure_set_theoretic_operations_menu_action(window: QMainWindow, parent: QMenu) -> QAction:
    menu = QMenu('Set-Theoretic', parent)

    menu.addActions([configure_action(window, 'Union', window.union_button_click),
                     configure_action(window, 'Intersection', window.intersection_button_click),
                     configure_action(window, 'Substraction', window.substraction_button_click)])

    return menu.menuAction()


def configure_algebraic_operations_menu_action(window: QMainWindow, parent: QMenu) -> QAction:
    menu = QMenu('Algebraic', parent)

    menu.addActions([configure_action(window, 'Operation', window.operation_button_click)])

    return menu.menuAction()


def configure_binary_operations_menu_action(window: QMainWindow, parent: QMenu) -> QAction:
    menu = QMenu('Binary', parent)

    menu.addActions([configure_set_theoretic_operations_menu_action(window, menu),
                     configure_algebraic_operations_menu_action(window, menu)])

    return menu.menuAction()


def configure_operations_menu_action(window: QMainWindow, parent: QMenuBar) -> QAction:
    menu = QMenu('Operations', parent)

    menu.addActions([configure_binary_operations_menu_action(window, menu)])

    return menu.menuAction()


def configure_menu_bar(window: QMainWindow) -> QMenuBar:
    bar = QMenuBar(window)

    bar.addActions([configure_file_menu_action(window, bar),
                    configure_operations_menu_action(window, bar)])

    return bar
