from PySide6.QtWidgets import QWidget, QTableWidget, QHBoxLayout, QTableWidgetItem


class ProjectTableWidget(QWidget):
    def __init__(self, data: list) -> None:
        super().__init__()

        header = ["项目编号", "项目名称", "创建时间", "修改时间", "删除", "项目文件数量", "项目文件占用空间", "文件一览"]

        self.table = QTableWidget()
        self.table.setColumnCount(len(header))
        self.table.setRowCount(len(data))

        self.table.setHorizontalHeaderLabels(header)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        for i in range(0, len(data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(data[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(data[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(data[i][4]))
            self.table.setItem(i, 3, QTableWidgetItem(data[i][3]))
            # self.table.setItem(i,0,QTableWidgetItem(data[i][0]))

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)
