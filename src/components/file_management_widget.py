import os
from typing import List
from PySide6 import QtCore
from PySide6.QtGui import QIcon, QAction, QCursor
from PySide6.QtWidgets import (
    QFrame,
    QToolButton,
    QMainWindow,
    QGridLayout,
    QMessageBox,
    QMenu,
)
from components.base_toolbutton import BaseToolButton
from components.file_widget import FileElementWidget
from components.folder_widget import FolderElementWidget

from models import Folder
from models.file_model import File
from constants import *


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
        self.__render()
        ## 可以文件拖拽进主窗体
        self.setAcceptDrops(True)

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
            f.moveFileSingal.connect(self.__handle_file_move)
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

        print(
            "children length:",
            len(
                list(
                    filter(
                        lambda x: type(x) is FileElementWidget
                        or type(x) is FolderElementWidget,
                        self.children(),
                    )
                )
            ),
        )
        # for i in self.children():
        #     print(type(i))

    def repaintByParent(self, repaint: bool = True):
        self.folder: Folder = self.parent.folder
        self.__render(repaint=repaint)

    def resizeEvent(self, event) -> None:
        self.__repaint()

    ## 文件移动事件
    def __handle_file_move(self, info: tuple):
        print(info)

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

    ## 拖拽文件
    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, e):
        filePathList = e.mimeData().text()
        filePath: str = filePathList.split("\n")[0]  # 拖拽多文件只取第一个地址
        # print(filePath)
        filePath = filePath.replace("file:///", "")

        if os.path.isfile(filePath):
            self.parent.folder.append(File(filePath))
            self.__render(True)

    def create_rightmenu(self):
        groupBoxMenu = QMenu(self)
        formatAction = QAction(QIcon(FORMAT_ICON), "刷新", self)
        formatAction.triggered.connect(self.__repaint)
        groupBoxMenu.addAction(formatAction)

        groupBoxMenu.popup(QCursor.pos())

    def mousePressEvent(self, event) -> None:
        if event.buttons() == QtCore.Qt.RightButton:
            self.create_rightmenu()
