import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem


class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.setGeometry(300, 300, 460, 380)
        self.setWindowTitle('Эспрессо')

        self.table()

        self.show()

    def table(self):
        con = sqlite3.connect("coffee.sqlite")
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
    ex = Coffee()
    ex.show()
    sys.exit(app.exec_())
