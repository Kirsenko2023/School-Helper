import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMainWindow


class BaseWindow(QMainWindow):
    def __init__(self, title='Расписание'):
        super().__init__()
        self.resize(1000, 1000)
        self.setWindowTitle('Расписание')
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)
        self.schedule_button = QPushButton('Расписание')
        self.schedule_button.move(50, 100)
        self.scores_button = QPushButton('Оценки')
        self.scores_button.move(150, 100)
        self.homework_button = QPushButton('Домашнее задание')
        self.homework_button.move(250, 100)
        self.schedule_button.clicked.connect(self.open_schedule)
        self.scores_button.clicked.connect(self.open_scores)
        self.homework_button.clicked.connect(self.open_homework)
        self.layout.addWidget(self.schedule_button)
        self.layout.addWidget(self.scores_button)
        self.layout.addWidget(self.homework_button)
        

    def open_schedule(self):
        self.open_windows(Schedule)

    def open_scores(self):
        self.open_windows(Scores)

    def open_homework(self):
        self.open_windows(Homework)

    def open_windows(self, window_class):
        self.next_window = window_class(self)
        self.next_window.show()
        self.close()

class SubWindow(QMainWindow):
    def __init__(self, parent_menu, title):
        super().__init__()
        self.parent_menu = parent_menu
        self.resize(1000, 1000)
        self.setWindowTitle(title)
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)
        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

    def go_back(self):
        self.parent_menu.show()
        self.hide()


class Schedule(SubWindow):
    def __init__(self, parent_menu):
        super().__init__(parent_menu, 'Расписание')


class Scores(SubWindow):
    def __init__(self, parent_menu):
        super().__init__(parent_menu, 'Оценки')


class Homework(SubWindow):
    def __init__(self, parent_menu):
        super().__init__(parent_menu, 'Домашнее задание')
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BaseWindow()
    ex.show()
    sys.exit(app.exec())
        