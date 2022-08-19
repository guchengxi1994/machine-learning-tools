from typing import List
from PySide6 import QtCore
from PySide6.QtWidgets import QFrame, QToolButton, QMainWindow, QGridLayout, QMessageBox
from components.base_toolbutton import BaseToolButton
from components.file_widget import FileElementWidget
from components.folder_widget import FolderElementWidget

from models import Folder


class FileManagementWidget(QFrame):
    elementWidth = 80
    elementHeight = 100

    def __init__(self, parent: QMainWindow) -> None:
        super(FileManagementWidget, self).__init__()
        self.setLineWidth(5)  # 设置外线宽度
        self.setMidLineWidth(3)  # 设置中线宽度
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)  # 根据延时表参数写入
        self.parent = parent
        self.__layout = QGridLayout()
        self.__layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setLayout(self.__layout)
        self.folder: Folder = self.parent.folder
        self.folder.append(Folder("1", [Folder("11", [])]))
        self.folder.append(Folder("2", []))
        self.folder.append(Folder("3", []))
        self.folder.append(Folder("4", []))
        self.folder.append(Folder("5", []))
        self.folder.append(Folder("6", []))
        self.folder.append(Folder("7", []))
        self.folder.append(Folder("8", []))
        self.folder.append(Folder("9", []))
        self.folder.append(Folder("10", []))
        self.__render()

    def __render(self, repaint: bool = False):
        if repaint:
            for i in self.elements:
                i.setParent(None)
                i.deleteLater()
                i = None

        self.elements: List[QToolButton] = []
        for i in self.folder.children:
            if type(i) is Folder:
                f = FolderElementWidget(i, self)
                f.doubleClickSignal.connect(self.__double_click)
            else:
                f = FileElementWidget(i, self)
                f.doubleClickSignal.connect(self.__double_click_file)
            f.rightClickSingal.connect(self.__handle_item_right_button_click)
            self.elements.append(f)

        elementLength = len(self.elements)
        __currentWindowWidth = self.parent.width() - 100

        rowCount = int(__currentWindowWidth / self.elementWidth)
        rows = int(elementLength / rowCount) + 1
        for i in range(rows):
            for j in range(rowCount):
                if i * rowCount + j >= elementLength:
                    break
                self.__layout.addWidget(self.elements[i * rowCount + j], i, j)

        print("children length:", len(self.children()))

    def repaintByParent(self, repaint: bool = True):
        self.folder: Folder = self.parent.folder
        self.__render(repaint=repaint)

    def resizeEvent(self, event) -> None:
        self.__repaint()

    def __double_click(self, info):
        _element = list(
            filter(
                lambda x: type(x) is FolderElementWidget
                and x.folder.folderName == info,
                self.elements,
            )
        )[0]
        self.folder: Folder = _element.folder
        self.parent.folderList.append(self.folder)
        self.__render(repaint=True)

    def __handle_item_right_button_click(self, info: tuple):
        _element: BaseToolButton
        for i in self.elements:
            if i.label == info[1]:
                _element = i
                break
        print(type(_element))
        m = QMessageBox()
        m.setText("是否要删除？")
        m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        m.setDefaultButton(QMessageBox.Yes)
        r = m.exec()
        # print(r)
        if r == QMessageBox.Yes:
            # print(".")
            self.parent.folder.remove(_element.T)
            self.__render(repaint=True)

    def __double_click_file(self, info):
        print("file", info)

    def __repaint(self):
        elementLength = len(self.elements)
        __currentWindowWidth = self.parent.width() - 100

        rowCount = int(__currentWindowWidth / self.elementWidth)
        rows = int(elementLength / rowCount) + 1
        for i in range(rows):
            for j in range(rowCount):
                if i * rowCount + j >= elementLength:
                    break
                self.__layout.removeWidget(self.elements[i * rowCount + j])
                self.__layout.addWidget(self.elements[i * rowCount + j], i, j)
