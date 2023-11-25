import openpyxl
import sys
from PyQt5 import QtWidgets, QtCore, uic
from random import *


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Главное меню')
        vbox = QtWidgets.QVBoxLayout(self)
        self.btn_select = QtWidgets.QPushButton('Выбрать количество заданий')
        self.btn_select.clicked.connect(self.open_modal_window)
        self.btn_select.setShortcut('Return')
        self.btn_start = QtWidgets.QPushButton('Начать тест')
        self.btn_start.clicked.connect(self.open_test_window)
        self.btn_start.setShortcut('Return')
        self.btn_start.setDisabled(True)
        self.btn_result = QtWidgets.QPushButton('Показать результаты')
        self.btn_result.clicked.connect(self.open_result_window)
        self.btn_result.setShortcut('Return')
        self.btn_result.setDisabled(True)
        self.num = 0
        vbox.addWidget(self.btn_select)
        vbox.addWidget(self.btn_start)
        vbox.addWidget(self.btn_result)
        self.resize(200, 200)
        self.show()

    def open_modal_window(self):
        ui1 = uic.loadUi('Task_Select.ui')
        ui1.label2.setText(
            f'Максимально возможное число: {len(tasks)():}')
        ui1.btnNext.clicked.connect(lambda: self.get_num(ui1))
        ui1.btnNext.clicked.connect(lambda: self.btn_select.setDisabled(True))
        ui1.btnNext.clicked.connect(lambda: self.btn_start.setDisabled(False))
        ui1.btnNext.clicked.connect(lambda: ui1.close())
        ui1.setWindowModality(QtCore.Qt.ApplicationModal)
        ui1.show()

    def get_num(self, ui):
        self.num = int(ui.lineEdit.text())

    def open_test_window(self):
        self.btn_start.setDisabled(True)
        self.w = TestWindow()
        n = choice(numbers)
        numbers.remove(n)
        num_task.append(n + 1)
        comp.append(answers[n])
        self.w.label.setText('\u0417\u0430\u0434\u0430\u0447\u0430 1')
        self.w.task.setText(tasks[n])
        self.w.option1.setText(options[n][0])
        self.w.option2.setText(options[n][1])
        self.w.option3.setText(options[n][2])
        self.w.option4.setText(options[n][3])
        self.w.show()

    def open_result_window(self):
        self.w1 = ResultWindow()
        self.close()


class TestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Test_Window.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.btnAnswer.clicked.connect(self.on_clicked)
        self.count = 1

    def on_clicked(self):
        global n  # inserted
        self.update()
        if self.count > window.num:
            self.close()
            window.btn_result.setDisabled(False)
        else:  # inserted
            if self.count == window.num:
                self.btnAnswer.setText('\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c')
                self.btnAnswer.setShortcut('Return')
                self.count += 1
                for i in range(1, 5):
                    attr = getattr(self, f'option{i}')
                    if attr.isChecked():
                        self.ans = attr.text()[3:]
                        break
            else:  # inserted
                n = choice(numbers)
                numbers.remove(n)
                comp.append(answers[n])
                num_task.append(n + 1)
                for i in range(1, 5):
                    attr = getattr(self, f'option{i}')
                    if i == 4:
                        attr2 = getattr(self, f'option{i - 1}')
                    else:  # inserted
                        attr2 = getattr(self, f'option{i + 1}')
                    if attr.isChecked():
                        self.ans = attr.text()[3:]
                        attr2.setChecked(True)
                        break
                self.label.setText(f'Задание {self.count + 1}')
                self.task.setText(tasks[n])
                self.option1.setText(options[n][0])
                self.option2.setText(options[n][1])
                self.option3.setText(options[n][2])
                self.option4.setText(options[n][3])
                self.count += 1
                num_answer.append(self.ans)


class ResultWindow(QtWidgets.QWidget):
    def __init__(self):
        global num_task  # inserted
        global points  # inserted
        super().__init__()
        uic.loadUi('Result_Window.ui', self)
        window.btn_result.setDisabled(True)
        for l in range(len(num_task)):
            if num_answer[l] == comp[l]:
                points.append('1')
            else:  # inserted
                points.append('0')
        num_task = [str(o) for o in num_task]
        self.lst = [num_task, num_answer, points]
        self.c = 0
        self.table.setRowCount(len(num_task))
        for el in self.lst:
            for m in range(len(num_task)):
                item = QtWidgets.QTableWidgetItem(el[m])
                self.table.setItem(m, self.c, item)
            self.c += 1
        points = [int(z) for z in points]
        summ = sum(points)
        self.text.setText(f'\u0412\u0441\u0435\u0433\u043e \u0431\u0430\u043b\u043b\u043e\u0432: {summ}')
        self.show()


app = QtWidgets.QApplication(sys.argv)
path = QtWidgets.QFileDialog().getOpenFileName()[0].replace('\"', '')
try:
    data = []
    tasks = []
    options = []
    answers = []
    comp = []
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    cell_obj = sheet_obj['A1':'C10']
    for cell1, cell2, cell3 in cell_obj:
        tasks.append(str(cell1.value))
        answers.append(str(cell2.value))
        options.append(str(cell3.value))
    numbers = [int(k) for k in range(0, len(tasks))]
    points = []
    num_task = []
    num_answer = []
    counter = 0
    for i in range(len(options)):
        options[i] = options[i].split(';  ')
    window = MainWindow()
except openpyxl.utils.exceptions.InvalidFileException:
    exit()
sys.exit(app.exec_())
