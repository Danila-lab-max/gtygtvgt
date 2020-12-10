import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QLabel, QLineEdit, QRadioButton
from PyQt5.QtGui import QPainter, QColor, QPen
from math import sqrt, factorial
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap


# Главное окно
class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('EasyMath')

        self.pixmap = QPixmap('1.png')
        self.image = QLabel(self)
        self.image.move(230, 80)
        self.image.resize(600, 600)
        self.image.setPixmap(self.pixmap)

        self.btn_calc = QPushButton('Калькулятор', self)
        self.btn_calc.resize(100, 100)
        self.btn_calc.move(50, 100)

        self.btn_func = QPushButton('Линейная функция', self)
        self.btn_func.resize(105, 100)
        self.btn_func.move(250, 100)

        self.btn_x_y = QPushButton('Формулы', self)
        self.btn_x_y.resize(100, 100)
        self.btn_x_y.move(450, 100)

        self.btn_calc.clicked.connect(self.open_calculator)
        self.btn_func.clicked.connect(self.open_function)
        self.btn_x_y.clicked.connect(self.open_formula)

    # Открывание других окон при нажатии кнопок
    def open_calculator(self):
        self.calculator_form = Calculator(self, 'Калькулятор')
        self.calculator_form.show()

    def open_function(self):
        self.function_form = Function(self, 'Построение линейной функции')
        self.function_form.show()

    def open_formula(self):
        self.formula_form = Formula(self, 'Формулы по математике')
        self.formula_form.show()


# Калькулятор
class Calculator(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('calc (4).ui', self)
        self.numbers = ['0', '0']
        self.i = 0
        self.operation = ''
        self.change = False
        self.last = ''

        self.setWindowTitle(args[-1])

        self.btn0.clicked.connect(lambda: self.get_number(self.btn0.text()))
        self.btn1.clicked.connect(lambda: self.get_number(self.btn1.text()))
        self.btn2.clicked.connect(lambda: self.get_number(self.btn2.text()))
        self.btn3.clicked.connect(lambda: self.get_number(self.btn3.text()))
        self.btn4.clicked.connect(lambda: self.get_number(self.btn4.text()))
        self.btn5.clicked.connect(lambda: self.get_number(self.btn5.text()))
        self.btn6.clicked.connect(lambda: self.get_number(self.btn6.text()))
        self.btn7.clicked.connect(lambda: self.get_number(self.btn7.text()))
        self.btn8.clicked.connect(lambda: self.get_number(self.btn8.text()))
        self.btn9.clicked.connect(lambda: self.get_number(self.btn9.text()))

        self.btn_clear.clicked.connect(self.clear)

        self.btn_plus.clicked.connect(lambda: self.operations(self.btn_plus.text()))
        self.btn_minus.clicked.connect(lambda: self.operations(self.btn_minus.text()))
        self.btn_mult.clicked.connect(lambda: self.operations(self.btn_mult.text()))
        self.btn_div.clicked.connect(lambda: self.operations(self.btn_div.text()))
        self.btn_pow.clicked.connect(lambda: self.operations(self.btn_pow.text()))
        self.btn_sqrt.clicked.connect(lambda: self.sqrt())
        self.btn_fact.clicked.connect(lambda: self.factorial())

        self.true_ravno = False

        self.btn_eq.clicked.connect(self.ravno)

        self.btn_clear.clicked.connect(self.clear)

        self.btn_dot.clicked.connect(self.dot)

        self.stil = False

    # Запись числа в дисплей
    def get_number(self, number):
        if self.change:
            self.table.display(None)
            self.change = False
        self.numbers[self.i] += number
        self.table.display(float(self.numbers[self.i]))

    # Получение операции
    def operations(self, operation):
        if self.i == 1 and self.numbers[1] != '':
            self.ravno()
            self.numbers[1] = ''
        self.operation = operation
        self.i = 1
        self.change = True
        self.last = self.numbers[1]
        self.stil = False

    # Квадратный корень
    def sqrt(self):
        try:
            self.numbers[0] = sqrt(float(self.numbers[0]))
            self.table.display(float(self.numbers[0]))
        except:
            self.table.display('Error')
            self.numbers[0] = '0'
            self.numbers[1] = '0'
            self.i = 0

    # Факториал
    def factorial(self):
        try:
            self.numbers[0] = factorial(float(self.numbers[0]))
            self.table.display(float(self.numbers[0]))
        except:
            self.table.display('Error')
            self.numbers[0] = '0'
            self.numbers[1] = '0'
            self.i = 0

    # Равно
    def ravno(self):
        try:
            if self.stil:
                self.numbers[1] = self.last
            if self.operation == '+':
                self.numbers[0] = float(self.numbers[0]) + float(self.numbers[1])
            elif self.operation == '-':
                self.numbers[0] = float(self.numbers[0]) - float(self.numbers[1])
            elif self.operation == '*':
                self.numbers[0] = float(self.numbers[0]) * float(self.numbers[1])
            elif self.operation == '/':
                self.numbers[0] = float(self.numbers[0]) / float(self.numbers[1])
            elif self.operation == '^':
                self.numbers[0] = float(self.numbers[0]) ** float(self.numbers[1])
            self.table.display(self.numbers[0])
            self.true_ravno = True
            self.numbers[0] = str(self.numbers[0])
            self.last = self.numbers[1]
            self.numbers[1] = ''
            self.stil = True
        except:
            self.table.display('Error')
            self.numbers[0] = '0'
            self.numbers[1] = '0'
            self.i = 0

    # Десятичная дробь
    def dot(self):
        self.numbers[self.i] += '.'
        self.table.display(float(self.numbers[self.i]))

    # Очистка дисплея
    def clear(self):
        self.numbers[0] = '0'
        self.numbers[1] = '0'
        self.table.display(0)
        self.i = 0


class Function(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()
        self.setWindowTitle(args[-1])

    def initUI(self):
        self.setGeometry(600, 600, 600, 600)

        self.lineEdit = QLineEdit(self)
        self.lineEdit_2 = QLineEdit(self)
        self.pushButton = QPushButton('Нарисовать', self)
        self.Label = QLabel('Линейная функция\n        y=kx+b', self)
        self.error = QLabel('', self)
        self.label_k = QLabel('K', self)
        self.label_b = QLabel('b', self)

        self.lineEdit.move(0, 0)
        self.lineEdit_2.move(0, 50)
        self.pushButton.move(0, 100)
        self.Label.move(250, 10)
        self.error.move(10, 200)
        self.Label.resize(140, 60)
        self.error.resize(90, 70)
        self.label_k.move(60, 0)
        self.label_b.move(60, 50)

        self.Label.setStyleSheet("""
                QWidget {
                    font-size: 14px;
                    }
                """)
        self.error.setStyleSheet("""
                        QWidget {
                            font-size: 19px;
                            color: red;
                            }
                        """)

        self.lineEdit.resize(50, 30)
        self.lineEdit_2.resize(50, 30)
        self.do_paint = False
        self.pushButton.clicked.connect(self.paint)

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw_flag(qp)
            qp.end()

    def paint(self):
        try:
            self.k = float(self.lineEdit.text())
            self.b = float(self.lineEdit_2.text())
            self.do_paint = True
            self.error.setText('')
            self.repaint()
        except ValueError:
            self.error.setText('Неверные\nданные')

    # Рисование функции
    def draw_flag(self, qp):
        qp.drawLine(350, 110, 350, 470)
        qp.drawLine(180, 280, 520, 280)
        y1 = 190
        for i in range(0, 16):
            qp.drawLine(y1, 270, y1, 290)
            y1 += 20
        x1 = 440
        for i in range(0, 16):
            qp.drawLine(340, x1, 360, x1)
            x1 -= 20
        X = 350
        Y = 280
        y_1 = Y - 20 * self.k * 4
        x_1 = 350 + 80
        y_2 = Y + 20 * self.k * 4
        x_2 = 350 - 80
        pen = QPen(Qt.red, 2)
        qp.setPen(pen)
        qp.drawLine(x_1, y_1 - (self.b * 20), x_2, y_2 - (self.b * 20))


class Formula(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('untitled13.ui', self)
        self.setWindowTitle(args[-1])

        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.lineEdit_3.hide()

        self.name = False
        self.sub = False
        self.form = False

        self.connection = sqlite3.connect("1.sqlite")
        self.pushButton.clicked.connect(self.select_data)
        self.checkBox.stateChanged.connect(self.change)
        self.checkBox_2.stateChanged.connect(self.change)
        self.checkBox_3.stateChanged.connect(self.change)
        self.pushButton_2.clicked.connect(self.add)
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_4.clicked.connect(self.change1)
        self.select_data()

    # Появление нужных полей
    def change(self):
        if self.checkBox.isChecked():
            self.lineEdit.show()
            self.name = True
        else:
            self.lineEdit.hide()
            self.name = False
        if self.checkBox_2.isChecked():
            self.lineEdit_2.show()
            self.form = True
        else:
            self.lineEdit_2.hide()
            self.form = False
        if self.checkBox_3.isChecked():
            self.lineEdit_3.show()
            self.sub = True
        else:
            self.lineEdit_3.hide()
            self.sub = False

    # Добавлении формулы в базу данных
    def add(self):
        # Диалоговое окно
        valid = QMessageBox.question(
            self, '', "Действительно хотите изменить таблицу?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.connection.cursor().execute("""INSERT INTO Math VALUES(?, ?, ?)""",
                                             (self.lineEdit_2.text(), self.lineEdit_3.text(),
                                              self.lineEdit.text()))
            self.connection.commit()

    # Удаление формулы из базы данных
    def delete(self):
        valid = QMessageBox.question(
            self, '', "Действительно хотите изменить таблицу?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            r = self.connection.cursor().execute("""SELECT * FROM Math""").fetchall()
            list = [x[2] for x in r]
            name, ok_pressed = QInputDialog.getText(self, "Введите название формулы",
                                                    "Название формулы?")
            if ok_pressed:
                if name in list:
                    self.connection.cursor().execute("""DELETE from Math
                                                    WHERE Name=?""", (name,))
                    self.connection.commit()
                else:
                    while True:
                        name, ok_pressed = QInputDialog.getText(self, "Введите название формулы",
                                                                "Нет такой формулы. Попробуйте ещё.")
                        if (not ok_pressed) or (ok_pressed and name in list):
                            self.connection.cursor().execute("""DELETE from Math
                                                                WHERE Name=?""", (name,))
                            self.connection.commit()
                            break

    # Вывод нужных нам формул
    def select_data(self):
        if self.sub:
            res = self.connection.cursor().execute("""SELECT * FROM Math
                                                   WHERE Subject=?""", (self.lineEdit_3.text(),)).fetchall()
        else:
            res = self.connection.cursor().execute("SELECT * FROM Math").fetchall()
        for i in range(len(res)):
            if self.name:
                if self.lineEdit.text() not in res[i][2]:
                    res[i] = None
            if self.form:
                if self.lineEdit_2.text() not in res[i][0]:
                    res[i] = None
        while True:
            if None not in res:
                break
            else:
                res.remove(None)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()

    def change1(self):
        self.form = Chamge(self, 'Изменение')
        self.form.show()


# Изменение формулы
class Chamge(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('untitled16.ui', self)
        self.setWindowTitle(args[-1])
        self.pushButton.clicked.connect(self.ch)
        self.connection = sqlite3.connect("1.sqlite")

    def ch(self):
        res = self.connection.cursor().execute("""SELECT * FROM Math""").fetchall()
        trer = False
        for el in res:
            if self.lineEdit.text() == el[2] or self.lineEdit_2.text() == el[0]:
                trer = True
                break
        if trer:
            self.connection.cursor().execute("""UPDATE Math
                                                SET 
                                                Name = ?,
                                                Formula = ?,
                                                Subject = ?
                                                WHERE Name = ? OR Formula = ?""", (self.lineEdit.text(),
                                                                                   self.lineEdit_2.text(),
                                                                                   self.lineEdit_3.text(),
                                                                                   self.lineEdit.text(),
                                                                                   self.lineEdit_2.text()))
            self.connection.commit()
        else:
            QMessageBox.question(
                self, '', "Нет такого элемента",
                QMessageBox.Yes, QMessageBox.No)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

