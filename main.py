import sqlite3
from PyQt5 import uic
import os
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QInputDialog
from main_ui import Ui_Form
from addEditCoffeeForm import Ui_Form1


class AddCoffee(QWidget, Ui_Form1):
    def __init__(self, parent=None):
        super(AddCoffee, self).__init__(parent)
        self.id = 0
        self.setupUi(self)
        self.pushButton3.clicked.connect(self.insert)

    def insert(self):
        path = os.pardir + '/data/coffee.sqlite'
        con = sqlite3.connect(path)
        cur = con.cursor()
        if not self.id:
            data = (self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                    self.lineEdit_4.text(), self.lineEdit_6.text(), self.lineEdit_5.text())
            cur.execute("INSERT INTO coffee(sort, roasting, ground, taste, price, volume)"
                        " VALUES(?, ?, ?, ?, ?, ?)", data)
        else:
            data = (self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                    self.lineEdit_4.text(), self.lineEdit_6.text(), self.lineEdit_5.text(), int(self.id))
            cur.execute("""UPDATE coffee SET
                        sort = ?,
                        roasting = ?,
                        ground = ?,
                        taste = ?,
                        price = ?,
                        volume = ?
                        WHERE id = ?""", data)
        con.commit()
        con.close()
        self.id = 0
        self.close()
        main_window.table()

    def open(self, id):
        path = os.pardir + '/data/coffee.sqlite'
        con = sqlite3.connect(path)
        cur = con.cursor()
        cofs = cur.execute("SELECT * from coffee WHERE id = ?", (id,)).fetchall()[0]
        self.lineEdit.setText(str(cofs[1]))
        self.lineEdit_2.setText(cofs[2])
        self.lineEdit_3.setText(cofs[3])
        self.lineEdit_4.setText(cofs[4])
        self.lineEdit_6.setText(str(cofs[5]))
        self.lineEdit_5.setText(str(cofs[6]))
        self.id = id


class Coffee(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Coffee, self).__init__(parent)
        self.setupUi(self)
        self.coffee = self

        self.setGeometry(300, 300, 460, 380)
        self.setWindowTitle('Эспрессо')
        self.pushButton.clicked.connect(self.add_coffee)
        self.pushButton_2.clicked.connect(self.edit_coffee)
        self.table()

        self.show()

    def add_coffee(self):
        self.new_coffee = AddCoffee()
        self.new_coffee.show()

    def edit_coffee(self):
        path = os.pardir + '/data/coffee.sqlite'
        con = sqlite3.connect(path)
        cur = con.cursor()
        cofs = cur.execute("""SELECT * from coffee""").fetchall()
        cof_id = map(str, [i[0] for i in cofs])
        i, okBtnPressed = QInputDialog.getItem(self, "Выберите номер для редактирования",
                                               "Номер кофе",
                                               cof_id, 1, False)
        if okBtnPressed:
            self.flag = True
            self.new_coffee.open(i)
            self.new_coffee.show()

    def table(self):
        path = os.pardir + '/data/coffee.sqlite'
        con = sqlite3.connect(path)
        cur = con.cursor()
        cur.execute("select * from coffee")
        rows = cur.fetchall()
        titles = cur.execute("""PRAGMA table_info(coffee)""").fetchall()
        header = [i[1] for i in titles]
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)
        for k in range(len(header)):
            self.tableWidget.horizontalHeaderItem(k).setTextAlignment(Qt.AlignHCenter)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Coffee()
    main_window.show()
    sys.exit(app.exec_())
