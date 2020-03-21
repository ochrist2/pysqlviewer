#!venv/bin/python

from PyQt5.QtWidgets import (
    QApplication, QDialog, QGridLayout,
    QHBoxLayout, QPushButton, QSizePolicy,
    QTableWidget, QTabWidget, QTextEdit,
    QWidget, QTableWidgetItem
)
import sys
from PyQt5.QtCore import pyqtSlot
from db import engine
import numpy as np
import sqlalchemy


class SQLViewer(QDialog):
    def __init__(self, parent=None):
        super(SQLViewer, self).__init__(parent)
        self.create_container()

        main_layout = QGridLayout()
        main_layout.addWidget(self.container, 5, 1)
        main_layout.setRowStretch(5, 1)
        main_layout.setColumnStretch(1, 1)
        self.setLayout(main_layout)
        self.setWindowTitle("pysqlviewer")

    @pyqtSlot()
    def query_db(self):
        query = self.container.findChildren(QTextEdit)[0].toPlainText()  
        db = engine.connect()
        results = db.execute(query)
        
        for clause in ['UPDATE', 'INSERT', 'DELETE']:
            if clause in query.upper():
                return
        columns = results.keys()
        results = np.array([r for r in results])
            
        self.container.findChildren(QTableWidget)[0]\
            .setRowCount(len(results) + 1)
        self.container.findChildren(QTableWidget)[0]\
            .setColumnCount(results.shape[1])

        for i, column in enumerate(columns):
            self.container.findChildren(QTableWidget)[0]\
                .setItem(0, i, QTableWidgetItem(str(column)))

        for i, row in enumerate(results):
            for j, item in enumerate(row):
                self.container.findChildren(QTableWidget)[0]\
                    .setItem(i + 1, j, QTableWidgetItem(str(item)))

    def create_container(self):
        self.container = QTabWidget()
        self.container.setSizePolicy(QSizePolicy.Preferred,
                                     QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("SELECT 1 as NUM")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        bb = QPushButton('Send query!')

        bb.clicked.connect(self.query_db)

        tab2hbox.addWidget(bb)
        tab2.setLayout(tab2hbox)

        self.container.addTab(tab2, "Enter query")
        self.container.addTab(tab1, "Query results")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = SQLViewer()
    gallery.show()
    sys.exit(app.exec_())
