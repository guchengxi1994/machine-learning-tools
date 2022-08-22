from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QTableWidgetItem,
    QPushButton,
)
from PySide6 import QtCore
from utils.get_project_path import get_project_path


class ProjectTableWidget(QWidget):
    closeSignal = QtCore.Signal(str)

    def __init__(self, data: list) -> None:
        super().__init__()
        header = ["项目编号", "项目名称", "创建时间", "修改时间", "删除", "项目文件数量", "项目文件占用空间", "文件一览"]

        self.table = QTableWidget()
        self.table.setColumnCount(len(header))
        self.table.setRowCount(len(data))
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(header)
        # self.table.setSelectionMode(QTableWidget.SingleSelection)

        for i in range(0, len(data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(data[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(data[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(data[i][4]))
            self.table.setItem(i, 3, QTableWidgetItem(data[i][3]))
            # self.table.setItem(i,0,QTableWidgetItem(data[i][0]))
            pushButton = QPushButton("打开此项目")
            pushButton.clicked.connect(self.__get_project_path)
            self.table.setCellWidget(i, 7, pushButton)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)

    def __get_project_path(self):
        button = self.sender()
        row = self.table.indexAt(button.pos()).row()
        rowId = self.table.item(row, 0).text()
        # print(rowId)
        s = get_project_path(int(rowId))
        if s != "":
            self.closeSignal.emit(s)
