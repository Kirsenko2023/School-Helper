import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton


class Arifmometr(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Arifmometr()
    ex.show()
    sys.exit(app.exec())
        