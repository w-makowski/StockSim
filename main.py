from PySide6.QtWidgets import (QApplication,
                               QMainWindow)
from controllers.main_controller import MainController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StockSim")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)


def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()


if __name__ == "__main__":
    app = QApplication([])

    stylesheet = load_stylesheet("gui/dark_theme.qss")
    app.setStyleSheet(stylesheet)

    main_window = MainWindow()
    main_controller = MainController(main_window)
    main_controller.add_stocks_to_db()
    main_controller.show_main_view()

    main_window.show()
    app.exec()
