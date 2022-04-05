import sys

from PyQt5.QtWidgets import QApplication

from src.main.frontend.main_view.view import MainView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec_())
