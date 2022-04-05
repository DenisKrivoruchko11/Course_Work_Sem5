from PyQt5.QtWidgets import QMenu, QMenuBar, QAction, QMainWindow

from src.main.frontend.common import configure_action, configure_choose_menu_action


def configure_file_menu_action(window: QMainWindow, parent: QMenuBar) -> QAction:
    menu = QMenu('File', parent)

    menu.addActions([configure_action(window, 'Set name', window.set_name_button_click),
                     configure_action(window, 'Save', window.save_button_click),
                     configure_choose_menu_action(window, menu, 'Open in main window', window.open_button_click)])

    return menu.menuAction()


def configure_menu_bar(window: QMainWindow) -> QMenuBar:
    bar = QMenuBar(window)

    bar.addActions([configure_file_menu_action(window, bar)])

    return bar
