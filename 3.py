import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog, QMessageBox, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit
from PyQt6.QtCore import Qt
from PyQt6 import uic
from ui_main_menu import Ui_MainWindow as Ui_MainMenu
from ui_schedule import Ui_MainWindow as Ui_Schedule
from ui_homework import Ui_HomeworkWindow as Ui_Homework
from ui_settings import Ui_MainWindow as Ui_Settings
from ui_add_lesson import Ui_Form as Ui_AddLesson


baze = 'grades.db'
ui_gr = 'grades_window.ui'
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
lesson_count = 8
bw_style = """
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-family: "Segoe UI", "Arial", sans-serif;
    font-size: 13px;
}
QMainWindow, QDialog { background-color: #2b2b2b; }
QPushButton {
    background-color: #3a3a3a; color: #ffffff;
    border: 1px solid #888888; border-radius: 4px;
    padding: 6px 14px; min-height: 20px;
}
QPushButton:hover { background-color: #ffffff; color: #2b2b2b; border: 1px solid #ffffff; }
QPushButton:pressed { background-color: #dddddd; color: #111111; }
QPushButton:disabled { background-color: #2f2f2f; color: #777777; border-color: #444444; }
QLineEdit, QPlainTextEdit, QTextEdit {
    background-color: #1e1e1e; color: #ffffff;
    border: 1px solid #888888; border-radius: 4px;
    padding: 4px 6px;
    selection-background-color: #ffffff; selection-color: #2b2b2b;
}
QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus {
    border: 2px solid #ffffff; padding: 3px 5px;
}
QLineEdit:disabled, QPlainTextEdit:disabled {
    background-color: #2a2a2a; color: #777777; border-color: #444444;
}
QComboBox {
    background-color: #1e1e1e; color: #ffffff;
    border: 1px solid #888888; border-radius: 4px;
    padding: 4px 8px; min-height: 20px;
}
QComboBox:hover { background-color: #3a3a3a; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent; border-right: 4px solid transparent;
    border-top: 5px solid #ffffff; width: 0; height: 0; margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #1e1e1e; color: #ffffff;
    border: 1px solid #ffffff;
    selection-background-color: #ffffff; selection-color: #2b2b2b;
    outline: none;
}
QTableWidget, QTableView {
    background-color: #1e1e1e; alternate-background-color: #262626;
    color: #ffffff; gridline-color: #555555;
    border: 1px solid #888888; border-radius: 4px;
    selection-background-color: #ffffff; selection-color: #2b2b2b;
    outline: none;
}
QTableWidget::item, QTableView::item { padding: 4px; border: none; }
QTableWidget::item:selected, QTableView::item:selected {
    background-color: #ffffff; color: #2b2b2b;
}
QHeaderView::section {
    background-color: #111111; color: #ffffff;
    padding: 6px; border: 1px solid #555555; font-weight: bold;
}
QTableCornerButton::section { background-color: #111111; border: 1px solid #555555; }
QScrollBar:vertical { background-color: #1e1e1e; width: 12px; margin: 0; border: none; }
QScrollBar::handle:vertical { background-color: #888888; min-height: 20px; border-radius: 4px; }
QScrollBar::handle:vertical:hover { background-color: #ffffff; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; background: none; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: #1e1e1e; }
QScrollBar:horizontal { background-color: #1e1e1e; height: 12px; margin: 0; border: none; }
QScrollBar::handle:horizontal { background-color: #888888; min-width: 20px; border-radius: 4px; }
QScrollBar::handle:horizontal:hover { background-color: #ffffff; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; background: none; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: #1e1e1e; }
QLabel { background-color: transparent; color: #ffffff; }
QMenuBar { background-color: #2b2b2b; color: #ffffff; border-bottom: 1px solid #555555; }
QMenuBar::item { background-color: transparent; padding: 4px 10px; }
QMenuBar::item:selected { background-color: #ffffff; color: #2b2b2b; }
QMenu { background-color: #2b2b2b; color: #ffffff; border: 1px solid #ffffff; }
QMenu::item:selected { background-color: #ffffff; color: #2b2b2b; }
QStatusBar { background-color: #2b2b2b; color: #ffffff; border-top: 1px solid #555555; }
QMessageBox { background-color: #2b2b2b; }
QMessageBox QLabel { color: #ffffff; }
QMessageBox QPushButton { min-width: 80px; }
QToolTip { background-color: #111111; color: #ffffff; border: 1px solid #ffffff; padding: 4px; }
QCheckBox, QRadioButton { background-color: transparent; color: #ffffff; spacing: 6px; }
QCheckBox::indicator, QRadioButton::indicator {
    width: 14px; height: 14px; border: 1px solid #ffffff; background-color: #1e1e1e;
}
QCheckBox::indicator:checked, QRadioButton::indicator:checked { background-color: #ffffff; }
QGroupBox {
    background-color: #1e1e1e; border: 1px solid #888888; border-radius: 6px;
    margin-top: 14px; padding: 10px 8px 8px 8px; font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 12px; padding: 0 6px; background-color: #2b2b2b; color: #ffffff;
}
QSpinBox {
    background-color: #1e1e1e; color: #ffffff;
    border: 1px solid #888888; border-radius: 4px;
    padding: 4px 6px; min-height: 20px;
}
QSpinBox:focus { border: 2px solid #ffffff; padding: 3px 5px; }
QSpinBox::up-button, QSpinBox::down-button {
    background-color: #3a3a3a; border: 1px solid #888888; width: 16px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover { background-color: #ffffff; }
QSpinBox::up-arrow {
    image: none;
    border-left: 4px solid transparent; border-right: 4px solid transparent;
    border-bottom: 5px solid #ffffff; width: 0; height: 0;
}
QSpinBox::down-arrow {
    image: none;
    border-left: 4px solid transparent; border-right: 4px solid transparent;
    border-top: 5px solid #ffffff; width: 0; height: 0;
}
"""


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
    conn.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def_settings = {
    'student_name': 'Ученик',
    'student_class': '',
    'theme': 'Тёмная',
    'font_size': '13',
    'lesson_count': '8',
}


def load_settings():
    conn = sqlite3.connect(baze)
    rows = conn.execute('SELECT key, value FROM settings').fetchall()
    conn.close()
    result = dict(def_settings)
    result.update(dict(rows))
    return result


def save_all_settings(settings_dict):
    conn = sqlite3.connect(baze)
    for key, value in settings_dict.items():
        conn.execute('''
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        ''', (key, str(value)))
    conn.commit()
    conn.close()


def apply_font_size(size_str):
    if str(size_str).isdigit():
        size = int(size_str)
    else:
        size = 13
    app = QApplication.instance()
    if app:
        app.setStyleSheet(bw_style.replace('font-size: 13px;', f'font-size: {size}px;', 1))


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
    subjects = []
    for (subject,) in rows:
        subjects.append(subject)
    return subjects


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
    col_names = {1: 'subject', 2: 'grade_date', 3: 'grade'}

    def __init__(self, on_back=None):
        super().__init__()
        uic.loadUi(ui_gr, self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Предмет', 'Дата', 'Оценка'])
        self.table.setColumnHidden(0, True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.add_button.clicked.connect(self.on_add_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.back_button.clicked.connect(on_back or self.close)
        self.table.itemChanged.connect(self.on_item_changed)
        self.refresh_table()

    def refresh_table(self):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        records = load_grades()
        self.table.setRowCount(len(records))
        for i, (gid, _full_name, subject, grade_date, grade) in enumerate(records):
            for j, value in enumerate([gid, subject, grade_date, grade]):
                item = QTableWidgetItem(str(value))
                if j in (0, 2, 3):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()
        self.table.blockSignals(False)

    def on_add_clicked(self):
        subject = self.subject_input.text()
        grade_date = self.date_input.text()
        grade_text = self.grade_input.text()
        if not subject or not grade_date:
            QMessageBox.warning(self, 'Ошибка', 'Заполните предмет и дату.')
            return
        if grade_text not in ('2', '3', '4', '5'):
            QMessageBox.warning(self, 'Ошибка', 'Оценка должна быть числом от 2 до 5.')
            return
        insert_grade(load_settings()['student_name'], subject, grade_date, int(grade_text))
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
        if QMessageBox.question(self, 'Подтверждение', 'Удалить выбранную оценку?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            delete_grade(grade_id)
            self.refresh_table()

    def on_item_changed(self, item):
        row, column = item.row(), item.column()
        grade_id = int(self.table.item(row, 0).text())
        column_name = self.col_names[column]
        new_value = item.text()
        if column_name == 'grade':
            if new_value not in ('2', '3', '4', '5'):
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
        for i in range(1, lesson_count + 1):
            self.combo_lesson.addItem(f'{i} урок')
        self.btn_save.clicked.connect(self.save_lesson)
        self.btn_cancel.clicked.connect(self.reject)
        if day:
            self.combo_day.setCurrentText(day)
        if lesson_num:
            self.combo_lesson.setCurrentIndex(lesson_num - 1)

    def save_lesson(self):
        subject = self.line_subject.text()
        if not subject:
            QMessageBox.warning(self, 'Ошибка', 'Введите предмет.')
            return
        upsert_lesson(self.combo_day.currentText(),
                      self.combo_lesson.currentIndex() + 1,
                      subject, self.line_room.text())
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
        header = QLabel(
            f'<b style="font-size:15px; color:#ffffff;">{subject}</b><br>'
            f'<span style="color:#aaaaaa;">{day}</span>'
        )
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

    def save(self):
        task = self.editor.toPlainText()
        if not task:
            QMessageBox.warning(self, 'Ошибка', 'Задание не может быть пустым.')
            return
        upsert_homework(self.subject, self.day, task)
        self.accept()

    def delete(self):
        if QMessageBox.question(self, 'Подтверждение', f'Удалить ДЗ по предмету «{self.subject}» на {self.day}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            delete_homework(self.subject, self.day)
            self.accept()


class SubWindow(QMainWindow):
    def __init__(self, ui_class, title, main_menu, with_schedule=False, with_homework=False, with_settings=False):
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
        if with_settings:
            self.setup_settings()

    def setup_schedule_table(self):
        table = self.ui.tableWidget
        table.setHorizontalHeaderLabels(days)
        labels = []
        for i in range(1, lesson_count + 1):
            labels.append(f'{i} урок')
        table.setVerticalHeaderLabels(labels)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def refresh_schedule(self):
        table = self.ui.tableWidget
        table.blockSignals(True)
        table.clearContents()
        for day, lesson_num, subject, room in load_schedule():
            row = lesson_num - 1
            if 0 <= row < table.rowCount():
                text = f'{subject} (каб. {room})' if room else subject
                table.setItem(row, days.index(day), QTableWidgetItem(text))
        table.blockSignals(False)

    def open_add_lesson(self):
        AddLessonWindow(self).exec()

    def delete_selected_lesson(self):
        row = self.ui.tableWidget.currentRow()
        col = self.ui.tableWidget.currentColumn()
        if row < 0 or col < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите урок в таблице.')
            return
        if QMessageBox.question(self, 'Подтверждение', f'Удалить урок {row + 1} ({days[col]})?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            delete_lesson(days[col], row + 1)
            self.refresh_schedule()

    def on_cell_double_clicked(self, row, col):
        dlg = AddLessonWindow(self, day=days[col], lesson_num=row + 1)
        item = self.ui.tableWidget.item(row, col)
        if item:
            text = item.text()
            if ' (каб. ' in text:
                subject, room = text.split(' (каб. ', 1)
                dlg.line_room.setText(room.rstrip(')'))
            else:
                subject = text
            dlg.line_subject.setText(subject)
        dlg.exec()

    def setup_homework_table(self):
        table = self.ui.tableWidget
        table.setHorizontalHeaderLabels(days)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setWordWrap(True)

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
                if entry:
                    text = entry[1]
                else:
                    text = ''
                item = QTableWidgetItem(text)
                if entry:
                    item.setToolTip(entry[1])
                else:
                    item.setForeground(Qt.GlobalColor.gray)
                table.setItem(row, col, item)
        table.blockSignals(False)

    def selected_homework_cell(self):
        row = self.ui.tableWidget.currentRow()
        col = self.ui.tableWidget.currentColumn()
        if row < 0 or col < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите ячейку в таблице.')
            return None
        item = self.ui.tableWidget.item(row, col)
        if item:
            task = item.text()
        else:
            task = ''
        return (self.ui.tableWidget.verticalHeaderItem(row).text(), days[col], task)

    def on_homework_add_clicked(self):
        subject, day, task = self.selected_homework_cell()
        if HomeworkDialog(self, subject, day, task).exec() == QDialog.DialogCode.Accepted:
            self.refresh_homework()

    def on_homework_delete_clicked(self):
        subject, day, task = self.selected_homework_cell()
        if not task:
            QMessageBox.information(self, 'Инфо', 'В этой ячейке нет задания.')
            return
        if QMessageBox.question(self, 'Подтверждение', f'Удалить ДЗ по предмету «{subject}» на {day}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            delete_homework(subject, day)
            self.refresh_homework()

    def on_homework_double_clicked(self, row, col):
        item = self.ui.tableWidget.item(row, col)
        subject = self.ui.tableWidget.verticalHeaderItem(row).text()
        day = days[col]
        if item:
            task = item.text()
        else:
            task = ''
        if HomeworkDialog(self, subject, day, task).exec() == QDialog.DialogCode.Accepted:
            self.refresh_homework()

    def setup_settings(self):
        ui = self.ui
        ui.combo_theme.addItems(['Тёмная', 'Светлая'])
        settings = load_settings()
        ui.line_student_name.setText(settings['student_name'])
        ui.line_student_class.setText(settings['student_class'])
        ui.combo_theme.setCurrentText(settings['theme'])
        ui.spin_font_size.setValue(int(settings['font_size']))
        ui.spin_lesson_count.setValue(int(settings['lesson_count']))
        ui.btn_save_settings.clicked.connect(self.on_save_settings)
        ui.btn_reset_settings.clicked.connect(self.on_reset_settings)

    def on_save_settings(self):
        global lesson_count
        ui = self.ui
        new_settings = {
            'student_name': ui.line_student_name.text(),
            'student_class': ui.line_student_class.text(),
            'theme': ui.combo_theme.currentText(),
            'font_size': str(ui.spin_font_size.value()),
            'lesson_count': str(ui.spin_lesson_count.value()),
        }
        save_all_settings(new_settings)
        apply_font_size(new_settings['font_size'])
        lesson_count = int(new_settings['lesson_count'])
        QMessageBox.information(self, 'Настройки', 'Настройки сохранены.')

    def on_reset_settings(self):
        global lesson_count
        if QMessageBox.question(self, 'Сброс', 'Сбросить все настройки по умолчанию?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        save_all_settings(def_settings)
        ui = self.ui
        ui.line_student_name.setText(def_settings['student_name'])
        ui.line_student_class.setText(def_settings['student_class'])
        ui.combo_theme.setCurrentText(def_settings['theme'])
        ui.spin_font_size.setValue(int(def_settings['font_size']))
        ui.spin_lesson_count.setValue(int(def_settings['lesson_count']))
        apply_font_size(def_settings['font_size'])
        lesson_count = int(def_settings['lesson_count'])
        QMessageBox.information(self, 'Настройки', 'Настройки сброшены.')

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

    def open_settings(self):
        self.open_ch(SubWindow(Ui_Settings, 'Настройки', self, with_settings=True))


if __name__ == '__main__':
    create_database()
    app = QApplication(sys.argv)
    settings = load_settings()
    apply_font_size(settings['font_size'])
    lesson_count = int(settings['lesson_count'])
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())