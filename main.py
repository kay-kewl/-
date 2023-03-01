import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QApplication


class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.update_table()

    def update_table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        results = cur.execute("select * from сорта").fetchall()
        if not results:
            return
        self.tableWidget.setColumnCount(len(results[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            "ID.название сорта.степень обжарки.молотый/в зернах.описание вкуса.цена.объем упаковки".split('.'))
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(results):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyForm()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
