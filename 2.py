import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QTableWidgetItem, 
                             QHeaderView, QAbstractItemView, QDialog)
from ui_main_menu import Ui_MainWindow as Ui_MainMenu
from ui_schedule import Ui_MainWindow as Ui_Schedule
from ui_scores import Ui_MainWindow as Ui_Scores
from ui_homework import Ui_MainWindow as Ui_Homework
from ui_reports import Ui_MainWindow as Ui_Reports
from ui_settings import Ui_MainWindow as Ui_Settings
from ui_add_lesson import Ui_Form as Ui_AddLesson 

class MainMenuWindow(QMainWindow, Ui_MainMenu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_schedule.clicked.connect(self.open_schedule)
        self.btn_scores.clicked.connect(self.open_scores)
        self.btn_homework.clicked.connect(self.open_homework)
        self.btn_reports.clicked.connect(self.open_reports)
        self.btn_settings.clicked.connect(self.open_settings)

    def open_schedule(self):
        self.schedule_window = SubWindow(Ui_Schedule, 'Расписание')
        self.schedule_window.show()
        self.close()

    def open_scores(self):
        self.scores_window = SubWindow(Ui_Scores, 'Оценки')
        self.scores_window.show()
        self.close()

    def open_homework(self):
        self.homework_window = SubWindow(Ui_Homework, 'Домашнее задание')
        self.homework_window.show()
        self.close()

    def open_reports(self):
        self.reports_window = SubWindow(Ui_Reports, 'Отчёты')
        self.reports_window.show()
        self.close()

    def open_settings(self):
        self.settings_window = SubWindow(Ui_Settings, 'Настройки')
        self.settings_window.show()
        self.close()


class AddLessonWindow(QDialog, Ui_AddLesson):
    def __init__(self, schedule_window):
        super().__init__()
        self.setupUi(self)
        self.schedule_window = schedule_window
        self.combo_day.addItems(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'])
        self.combo_lesson.addItems(['1 урок', '2 урок', '3 урок', '4 урок', '5 урок', '6 урок', '7 урок', '8 урок'])
        self.btn_save.clicked.connect(self.save_lesson)
        self.btn_cancel.clicked.connect(self.reject)

    def save_lesson(self):
        day_index = self.combo_day.currentIndex()
        lesson_index = self.combo_lesson.currentIndex()
        subject = self.line_subject.text()
        room = self.line_room.text()
        if not subject:
            return 
        cell_text = subject
        if room:
            cell_text = f'{subject} (каб. {room})'
        table = self.schedule_window.ui.tableWidget
        table.setItem(lesson_index, day_index, QTableWidgetItem(cell_text))
        self.close()


class SubWindow(QMainWindow):
    def __init__(self, ui_class, title):
        super().__init__()
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.btn_back.clicked.connect(self.go_back)
        if title == 'Расписание':
            self.setup_schedule_table()
            self.ui.btn_add_lesson.clicked.connect(self.open_add_lesson)

    def setup_schedule_table(self):
        table = self.ui.tableWidget
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        table.setHorizontalHeaderLabels(days)
        lessons = ['1 урок', '2 урок', '3 урок', '4 урок', '5 урок', '6 урок', '7 урок', '8 урок']
        table.setVerticalHeaderLabels(lessons)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        schedule_data = [
            ['Математика', 'Русский язык', 'Физика', 'История', 'Английский', ''],
            ['Литература','Математика', 'Химия', 'Физкультура', 'Биология', ''],
        ]
        for i, j in enumerate(schedule_data):
            for k, r in enumerate(j):
                if r:
                    table.setItem(i, k, QTableWidgetItem(r))
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def open_add_lesson(self):
        self.add_lesson_dialog = AddLessonWindow(self)
        self.add_lesson_dialog.exec()

    def go_back(self):
        self.menu = MainMenuWindow()
        self.menu.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())