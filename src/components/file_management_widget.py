import os
from typing import List
from PySide6 import QtCore
from PySide6.QtGui import QIcon, QAction, QCursor
from PySide6.QtWidgets import (
    QMainWindow,
    QGridLayout,
    QHBoxLayout,
    QMessageBox,
    QMenu,
    QWidget,
    QScrollArea,
    QInputDialog,
)
from components.base_toolbutton import BaseToolButton
from components.file_widget import FileElementWidget
from components.folder_widget import FolderElementWidget

from models import Folder
from models.file_model import File
from constants import *

SCROLLAREA_MARGIN = 175


class FileManagementWidget(QWidget):
    elementWidth = 80
    elementHeight = 70
    ## 新窗口打开子文件夹
    navigateSingal = QtCore.Signal(Folder)

    def __init__(self, parent: QMainWindow) -> None:
        super(FileManagementWidget, self).__init__()
        self.parent = parent

        self.mainLayout = QHBoxLayout(self)

        ## 添加滚动区域
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.contents = QWidget()

        self.scrollArea.setWidget(self.contents)

        self.__layout = QGridLayout(self.contents)
        self.__layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # self.setLayout(self.__layout)
        self.mainLayout.addWidget(self.scrollArea)
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

        self.elements: List[BaseToolButton] = []
        for i in self.parent.folderList[-1].children:
            if type(i) is Folder:
                f = FolderElementWidget(i, self)
                f.doubleClickSignal.connect(self.__double_click)
                f.navigateSingal.connect(self.__handle_navigate)
            else:
                f = FileElementWidget(i, self)
                f.doubleClickSignal.connect(self.__double_click_file)
            f.rightClickSingal.connect(self.__handle_item_right_button_click)
            f.moveFileSingal.connect(self.__handle_file_move)
            self.elements.append(f)

        elementLength = len(self.elements)
        __currentWindowWidth = self.parent.width() - SCROLLAREA_MARGIN

        rowCount = int(__currentWindowWidth / self.elementWidth)
        rows = int(elementLength / rowCount) + 1
        for i in range(rows):
            for j in range(rowCount):
                if i * rowCount + j >= elementLength:
                    break
                self.__layout.addWidget(self.elements[i * rowCount + j], i, j)

        # print(
        #     "children length:",
        #     len(
        #         list(
        #             filter(
        #                 lambda x: type(x) is FileElementWidget
        #                 or type(x) is FolderElementWidget,
        #                 self.children(),
        #             )
        #         )
        #     ),
        # )
        # for i in self.children():
        #     print(type(i))

    def repaintByParent(self, repaint: bool = True):
        # self.folder: Folder = self.parent.folder
        self.folder = self.parent.folderList[-1]
        self.__render(repaint=repaint)

    def resizeEvent(self, event) -> None:
        self.__repaint()

    ## 文件移动事件
    def __handle_file_move(self, info: tuple):
        print(info)
        resultList: List[FolderElementWidget] = []
        for i in self.elements:
            ## 文件夹是不能移入文件的
            if type(i) is not FolderElementWidget:
                continue
            if i.label == info[2]:
                continue
            ## 这里只判断左上角的点在另一个文件夹中间的情况
            if (
                i.pos().x() < info[0]
                and i.pos().x() + 0.5 * self.elementWidth > info[0]
                and i.pos().y() < info[1]
                and i.pos().y() + 0.5 * self.elementHeight > info[1]
            ):
                resultList.append(i)
        ## 如果已经有两个文件夹重叠了，那么就无法移入
        if len(resultList) == 1:
            m = QMessageBox()
            m.setText("是否要将{}移入{}?".format(info[2], resultList[0].label))
            m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m.setDefaultButton(QMessageBox.No)
            r = m.exec()

            if r == QMessageBox.Yes:
                _element: BaseToolButton
                for i in self.elements:
                    if i.label == info[2]:
                        _element = i
                        break
                if _element.T not in resultList[0].folder.children:
                    self.parent.folderList[-1].remove(_element.T)
                    resultList[0].folder.append(_element.T)
                    self.__render(repaint=True)

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
        __currentWindowWidth = self.parent.width() - SCROLLAREA_MARGIN

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
            self.parent.folderList[-1].append(File(filePath))
            self.__render(True)

    def create_rightmenu(self):
        groupBoxMenu = QMenu(self)
        formatAction = QAction(QIcon(FORMAT_ICON), "刷新", self)
        formatAction.triggered.connect(self.__repaint)
        createFolderAction = QAction(QIcon(CREATE_FOLDER_ICON), "新建文件夹", self)
        createFolderAction.triggered.connect(self.__create_new_folder)

        groupBoxMenu.addAction(formatAction)
        groupBoxMenu.addAction(createFolderAction)
        groupBoxMenu.popup(QCursor.pos())

    def mousePressEvent(self, event) -> None:
        if event.buttons() == QtCore.Qt.RightButton:
            self.create_rightmenu()

    ## 创建一个逻辑文件夹
    def __create_new_folder(self):
        text, ok = QInputDialog.getText(self, "输入文件夹名称", "输入")
        if ok and text is not None and text != "":
            # print(text)
            self.parent.folderList[-1].append(Folder(folderName=text, children=[]))
            self.__render(True)

    def __handle_navigate(self, info: Folder):
        # print(info)
        self.navigateSingal.emit(info)
