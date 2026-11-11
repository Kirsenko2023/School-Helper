import os
import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog, QMessageBox, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit
from PyQt6.QtCore import Qt
from PyQt6 import uic
from ui_main_menu import Ui_MainWindow as Ui_MainMenu
from ui_schedule import Ui_MainWindow as Ui_Schedule
from ui_homework import Ui_HomeworkWindow as Ui_Homework
from ui_reports import Ui_MainWindow as Ui_Reports
from ui_settings import Ui_MainWindow as Ui_Settings
from ui_add_lesson import Ui_Form as Ui_AddLesson


baze = 'grades.db'
ui_gr = 'grades_window.ui'
allowed = {'full_name', 'subject', 'grade_date', 'grade'}
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']


def create_database():
    conn = sqlite3.connect(baze)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            grade_date TEXT NOT NULL,
            grade INTEGER NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            lesson_num INTEGER NOT NULL,
            subject TEXT NOT NULL,
            room TEXT,
            UNIQUE(day, lesson_num)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            day TEXT NOT NULL,
            task TEXT NOT NULL,
            UNIQUE(subject, day)
        )
    ''')
    conn.commit()
    conn.close()


def load_grades():
    conn = sqlite3.connect(baze)
    rows = conn.execute('SELECT id, full_name, subject, grade_date, grade FROM grades').fetchall()
    conn.close()
    return rows


def insert_grade(full_name, subject, grade_date, grade):
    conn = sqlite3.connect(baze)
    conn.execute('INSERT INTO grades (full_name, subject, grade_date, grade) VALUES (?, ?, ?, ?)', (full_name, subject, grade_date, grade))
    conn.commit()
    conn.close()


def update_grade(grade_id, column, value):
    conn = sqlite3.connect(baze)
    conn.execute(f'UPDATE grades SET {column} = ? WHERE id = ?', (value, grade_id))
    conn.commit()
    conn.close()


def delete_grade(grade_id):
    conn = sqlite3.connect(baze)
    conn.execute('DELETE FROM grades WHERE id = ?', (grade_id,))
    conn.commit()
    conn.close()


def load_schedule():
    conn = sqlite3.connect(baze)
    rows = conn.execute('SELECT day, lesson_num, subject, room FROM schedule').fetchall()
    conn.close()
    return rows


def upsert_lesson(day, lesson_num, subject, room):
    conn = sqlite3.connect(baze)
    conn.execute('''
        INSERT INTO schedule (day, lesson_num, subject, room)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(day, lesson_num)
        DO UPDATE SET subject = excluded.subject, room = excluded.room
    ''', (day, lesson_num, subject, room))
    conn.commit()
    conn.close()


def delete_lesson(day, lesson_num):
    conn = sqlite3.connect(baze)
    conn.execute('DELETE FROM schedule WHERE day = ? AND lesson_num = ?', (day, lesson_num))
    conn.commit()
    conn.close()


def load_homework_subjects():
    conn = sqlite3.connect(baze)
    rows = conn.execute('SELECT DISTINCT subject FROM schedule ORDER BY subject').fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append(r[0])
    return result


def load_homework():
    conn = sqlite3.connect(baze)
    rows = conn.execute('SELECT id, subject, day, task FROM homework').fetchall()
    conn.close()
    result = {}
    for hw_id, subject, day, task in rows:
        result[(subject, day)] = (hw_id, task)
    return result


def upsert_homework(subject, day, task):
    conn = sqlite3.connect(baze)
    conn.execute('''
        INSERT INTO homework (subject, day, task)
        VALUES (?, ?, ?)
        ON CONFLICT(subject, day)
        DO UPDATE SET task = excluded.task
    ''', (subject, day, task))
    conn.commit()
    conn.close()


def delete_homework(subject, day):
    conn = sqlite3.connect(baze)
    conn.execute('DELETE FROM homework WHERE subject = ? AND day = ?', (subject, day))
    conn.commit()
    conn.close()


class GradesWindow(QWidget):
    col_names = {1: 'full_name', 2: 'subject', 3: 'grade_date', 4: 'grade'}
    def __init__(self, on_back=None):
        super().__init__()
        uic.loadUi(ui_gr, self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'ФИО', 'Предмет', 'Дата', 'Оценка'])
        self.table.setColumnHidden(0, True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.add_button.clicked.connect(self.on_add_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        if on_back:
            self.back_button.clicked.connect(on_back)
        else:
            self.back_button.clicked.connect(self.close)
        self.table.itemChanged.connect(self.on_item_changed)
        self.refresh_table()

    def refresh_table(self):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        records = load_grades()
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            for j, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                if j in (0, 3, 4):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()
        self.table.blockSignals(False)

    def on_add_clicked(self):
        full_name = self.name_input.text()
        subject = self.subject_input.text()
        grade_date = self.date_input.text()
        grade_text = self.grade_input.text()
        if not full_name or not subject or not grade_date:
            QMessageBox.warning(self, 'Ошибка', 'Заполните ФИО, предмет и дату.')
            return
        if not grade_text.isdigit() or not 2 <= int(grade_text) <= 5:
            QMessageBox.warning(self, 'Ошибка', 'Оценка должна быть числом от 2 до 5.')
            return
        insert_grade(full_name, subject, grade_date, int(grade_text))
        self.name_input.clear()
        self.subject_input.clear()
        self.date_input.clear()
        self.grade_input.clear()
        self.refresh_table()

    def on_delete_clicked(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите запись в таблице.')
            return
        grade_id = int(self.table.item(row, 0).text())
        answer = QMessageBox.question(self, 'Подтверждение', 'Удалить выбранную оценку?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            delete_grade(grade_id)
            self.refresh_table()

    def on_item_changed(self, item):
        row = item.row()
        column = item.column()
        if column == 0:
            return
        grade_id = int(self.table.item(row, 0).text())
        column_name = self.col_names[column]
        new_value = item.text()
        if column_name == 'grade':
            if not new_value.isdigit() or not 2 <= int(new_value) <= 5:
                QMessageBox.warning(self, 'Ошибка', 'Оценка должна быть числом от 2 до 5.')
                self.refresh_table()
                return
            new_value = int(new_value)
        update_grade(grade_id, column_name, new_value)


class AddLessonWindow(QDialog, Ui_AddLesson):
    def __init__(self, schedule_window, day=None, lesson_num=None):
        super().__init__()
        self.setupUi(self)
        self.schedule_window = schedule_window
        self.combo_day.addItems(days)
        for i in range(1, 9):
            self.combo_lesson.addItem(f'{i} урок')
        self.btn_save.clicked.connect(self.save_lesson)
        self.btn_cancel.clicked.connect(self.reject)
        if day is not None:
            self.combo_day.setCurrentText(day)
        if lesson_num is not None:
            self.combo_lesson.setCurrentIndex(lesson_num - 1)

    def save_lesson(self):
        subject = self.line_subject.text()
        room = self.line_room.text()
        if not subject:
            QMessageBox.warning(self, 'Ошибка', 'Введите предмет.')
            return
        day = self.combo_day.currentText()
        lesson_num = self.combo_lesson.currentIndex() + 1
        upsert_lesson(day, lesson_num, subject, room)
        self.schedule_window.refresh_schedule()
        self.accept()


class HomeworkDialog(QDialog):
    def __init__(self, parent=None, subject='', day='', task=''):
        super().__init__(parent)
        self.setWindowTitle(f'Домашнее задание — {subject} ({day})')
        self.resize(600, 400)
        self.subject = subject
        self.day = day
        layout = QVBoxLayout(self)
        header = QLabel(f'<b style="font-size:15px;">{subject}</b><br><span style="color:#666;">{day}</span>')
        header.setWordWrap(True)
        layout.addWidget(header)
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText('Введите домашнее задание...')
        self.editor.setPlainText(task)
        layout.addWidget(self.editor, 1)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_save = QPushButton('Сохранить')
        self.btn_delete = QPushButton('Удалить')
        self.btn_cancel = QPushButton('Отмена')
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_delete.clicked.connect(self.delete)
        self.setStyleSheet('''
            QPlainTextEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background: #fafafa;
            }
            QPushButton {
                padding: 6px 14px;
                border-radius: 6px;
                border: 1px solid #bbb;
                background: #f0f0f0;
            }
            QPushButton:hover { background: #e0e0e0; }
            QPushButton#btn_save { background: #cdeacd; }
            QPushButton#btn_save:hover { background: #b7dcb7; }
            QPushButton#btn_delete { background: #f4cccc; }
            QPushButton#btn_delete:hover { background: #ecb3b3; }
        ''')
        self.btn_save.setObjectName('btn_save')
        self.btn_delete.setObjectName('btn_delete')

    def save(self):
        task = self.editor.toPlainText()
        if not task:
            QMessageBox.warning(self, 'Ошибка', 'Задание не может быть пустым.')
            return
        upsert_homework(self.subject, self.day, task)
        self.accept()

    def delete(self):
        answer = QMessageBox.question(self, 'Подтверждение', f'Удалить ДЗ по предмету «{self.subject}» на {self.day}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            delete_homework(self.subject, self.day)
            self.accept()


class SubWindow(QMainWindow):
    def __init__(self, ui_class, title, main_menu, with_schedule=False, with_homework=False):
        super().__init__()
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.main_menu = main_menu
        self.ui.btn_back.clicked.connect(self.go_back)

        if with_schedule:
            self.setup_schedule_table()
            self.ui.btn_add_lesson.clicked.connect(self.open_add_lesson)
            self.ui.btn_delete_lesson.clicked.connect(self.delete_selected_lesson)
            self.ui.tableWidget.cellDoubleClicked.connect(self.on_cell_double_clicked)
            self.refresh_schedule()

        if with_homework:
            self.setup_homework_table()
            self.ui.btn_add_homework.clicked.connect(self.on_homework_add_clicked)
            self.ui.btn_delete_homework.clicked.connect(self.on_homework_delete_clicked)
            self.ui.tableWidget.cellDoubleClicked.connect(self.on_homework_double_clicked)
            self.refresh_homework()

    def setup_schedule_table(self):
        table = self.ui.tableWidget
        table.setHorizontalHeaderLabels(days)
        table.setVerticalHeaderLabels([f'{i} урок' for i in range(1, 9)])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def refresh_schedule(self):
        table = self.ui.tableWidget
        table.blockSignals(True)
        table.clearContents()
        for day, lesson_num, subject, room in load_schedule():
            col = days.index(day)
            row = lesson_num - 1
            if 0 <= row < table.rowCount():
                text = f'{subject} (каб. {room})' if room else subject
                table.setItem(row, col, QTableWidgetItem(text))
        table.blockSignals(False)

    def open_add_lesson(self):
        AddLessonWindow(self).exec()

    def delete_selected_lesson(self):
        row = self.ui.tableWidget.currentRow()
        col = self.ui.tableWidget.currentColumn()
        if row < 0 or col < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите урок в таблице.')
            return
        day = days[col]
        lesson_num = row + 1
        answer = QMessageBox.question(self, 'Подтверждение', f'Удалить урок {lesson_num} ({day})?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            delete_lesson(day, lesson_num)
            self.refresh_schedule()

    def on_cell_double_clicked(self, row, col):
        day = days[col]
        lesson_num = row + 1
        dlg = AddLessonWindow(self, day=day, lesson_num=lesson_num)
        item = self.ui.tableWidget.item(row, col)
        if item:
            text = item.text()
            if ' (каб. ' in text:
                subject, room_part = text.split(' (каб. ', 1)
                room = room_part.rstrip(')')
            else:
                subject, room = text, ''
            dlg.line_subject.setText(subject)
            dlg.line_room.setText(room)
        dlg.exec()

    def setup_homework_table(self):
        table = self.ui.tableWidget
        table.setHorizontalHeaderLabels(days)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setWordWrap(True)
        table.setStyleSheet('''
            QTableWidget {
                font-size: 13px;
                gridline-color: #ccc;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QHeaderView::section {
                background: #eef2f7;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #ccc;
            }
        ''')

    def refresh_homework(self):
        table = self.ui.tableWidget
        table.blockSignals(True)
        table.clearContents()
        subjects = load_homework_subjects()
        table.setRowCount(len(subjects))
        table.setVerticalHeaderLabels(subjects)
        hw = load_homework()
        for row, subject in enumerate(subjects):
            for col, day in enumerate(days):
                entry = hw.get((subject, day))
                if entry and entry[1]:
                    item = QTableWidgetItem(entry[1])
                    item.setToolTip(entry[1])
                else:
                    item = QTableWidgetItem('')
                    item.setForeground(Qt.GlobalColor.gray)
                table.setItem(row, col, item)
        table.blockSignals(False)

    def selected_homework_cell(self):
        row = self.ui.tableWidget.currentRow()
        col = self.ui.tableWidget.currentColumn()
        if row < 0 or col < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите ячейку в таблице.')
            return None
        subject = self.ui.tableWidget.verticalHeaderItem(row).text()
        day = days[col]
        item = self.ui.tableWidget.item(row, col)
        if item:
            task = item.text()
        else:
            task = ''
        return subject, day, task

    def on_homework_add_clicked(self):
        cell = self.selected_homework_cell()
        subject, day, task = cell
        dlg = HomeworkDialog(self, subject=subject, day=day, task=task)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.refresh_homework()

    def on_homework_delete_clicked(self):
        cell = self.selected_homework_cell()
        subject, day, task = cell
        if not task:
            QMessageBox.information(self, 'Инфо', 'В этой ячейке нет задания.')
            return
        answer = QMessageBox.question(self, 'Подтверждение', f'Удалить ДЗ по предмету «{subject}» на {day}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            delete_homework(subject, day)
            self.refresh_homework()

    def on_homework_double_clicked(self, row, col):
        subject = self.ui.tableWidget.verticalHeaderItem(row).text()
        day = days[col]
        item = self.ui.tableWidget.item(row, col)
        if item:
            task = item.text()
        else:
            task = ''
        dlg = HomeworkDialog(self, subject=subject, day=day, task=task)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.refresh_homework()

    def go_back(self):
        self.main_menu.show()
        self.close()


class MainMenuWindow(QMainWindow, Ui_MainMenu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_schedule.clicked.connect(self.open_schedule)
        self.btn_scores.clicked.connect(self.open_scores)
        self.btn_homework.clicked.connect(self.open_homework)
        self.btn_reports.clicked.connect(self.open_reports)
        self.btn_settings.clicked.connect(self.open_settings)
        self.child = None

    def open_ch(self, window):
        if self.child:
            self.child.close()
        self.child = window
        window.show()
        self.hide()

    def return_menu(self):
        if self.child:
            self.child.close()
            self.child = None
        self.show()

    def open_schedule(self):
        self.open_ch(SubWindow(Ui_Schedule, 'Расписание', self, with_schedule=True))

    def open_scores(self):
        self.open_ch(GradesWindow(on_back=self.return_menu))

    def open_homework(self):
        self.open_ch(SubWindow(Ui_Homework, 'Домашнее задание', self, with_homework=True))

    def open_reports(self):
        self.open_ch(SubWindow(Ui_Reports, 'Отчёты', self))

    def open_settings(self):
        self.open_ch(SubWindow(Ui_Settings, 'Настройки', self))


if __name__ == '__main__':
    create_database()
    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())