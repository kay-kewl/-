import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QApplication


class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.update_table()
        self.btn.clicked.connect(self.edit_coffee)
        self.btn1.clicked.connect(self.add_coffee)

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

    def add_coffee(self):
        self.window = EditForm(self)
        self.window.show()

    def edit_coffee(self):
        rows = [x.row() for x in self.tableWidget.selectedItems()]
        if len(rows) == 0 or len(rows) > 1:
            pass
        else:
            row = rows[0]
            params = [self.tableWidget.item(row, i).text() for i in range(7)]
            self.window = EditForm(self, *params)
            self.window.show()


class EditForm(QMainWindow):
    def __init__(self, window, *params):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.coffee = 0
        self.w = window
        self.edits = [self.edit1, self.edit2, self.edit3, self.edit4, self.edit5, self.edit6]
        self.new = True
        params = list(params)
        if params:
            self.coffee = params.pop(0)
            for i in range(len(params)):
                self.edits[i].setText(params[i])
            self.new = False
        self.btn.clicked.connect(self.save_changes)

    def save_changes(self):
        vs = [i.text() for i in self.edits]
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if not self.coffee:
            self.coffee = max([x[0] for x in cur.execute('select id from сорта').fetchall()]) + 1
        try:
            if self.new:
                cur.execute(
                    f"insert into сорта (id, название, обжарка, вид, вкус, цена, объем) "
                    f"values ('{self.coffee}', '{vs[0]}', '{vs[1]}', '{vs[2]}', '{vs[3]}', {vs[4]}, {vs[5]})")
            else:
                cur.execute(
                    f"update сорта set название = '{vs[0]}', обжарка = '{vs[1]}', вид = '{vs[2]}', "
                    f"вкус = '{vs[3]}', цена = {vs[4]}, объем = {vs[5]} where id = {self.coffee}")
            con.commit()
            self.w.update_table()
            self.close()
        except sqlite3.OperationalError as e:
            self.label.setText("ошибка")
        con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyForm()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
