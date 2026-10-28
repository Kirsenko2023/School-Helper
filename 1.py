import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton


class Arifmomet(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Arifmomet()
    ex.show()
    sys.exit(app.exec())
        