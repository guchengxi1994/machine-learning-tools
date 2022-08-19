from typing import TypeVar
from PySide6.QtWidgets import QToolButton, QMenu
from PySide6 import QtCore
from PySide6.QtGui import QIcon, QAction, QCursor
from models import Folder, File
from constants import *

FileOrFolder = TypeVar("FileOrFolder", File, Folder)


class BaseToolButton(QToolButton):
    doubleClickSignal = QtCore.Signal(str)
    rightClickSingal = QtCore.Signal(tuple)
    ## item 移动事件，可能移入文件夹中
    moveFileSingal = QtCore.Signal(tuple)

    def __init__(self, T: FileOrFolder, parent) -> None:
        super().__init__(parent)
        if type(T) is File:
            self.setText(T.fileName)
            self.label = T.fileName
            self.setIcon(QIcon(FILE_ICON))
        else:
            self.setText(T.folderName)
            self.label = T.folderName
            self.setIcon(QIcon(FOLDER_ICON))
        self.setIconSize(QtCore.QSize(32, 32))
        self.setFixedWidth(80)
        self.setFixedHeight(70)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("border : none")
        self.iniDragCor = [0, 0]
        self.T = T

    def mousePressEvent(self, e) -> None:
        # print("start", self.pos())
        self.iniDragCor[0] = e.x()
        self.iniDragCor[1] = e.y()

    def mouseReleaseEvent(self, e) -> None:
        # print("end", self.pos())
        self.moveFileSingal.emit((self.pos().x(), self.pos().y()))

    def mouseDoubleClickEvent(self, event) -> None:
        self.doubleClickSignal.emit(self.label)

    def mouseMoveEvent(self, e) -> None:
        x = e.x() - self.iniDragCor[0]
        y = e.y() - self.iniDragCor[1]
        cor = QtCore.QPoint(x, y)
        self.move(self.mapToParent(cor))  # 需要maptoparent一下才可以的,否则只是相对位置。

    def create_rightmenu(self):
        groupBoxMenu = QMenu(self)
        deleteAction = QAction(QIcon(DELETE_ICON), "删除数据", self)
        deleteAction.triggered.connect(self.__delete_item)
        groupBoxMenu.addAction(deleteAction)

        groupBoxMenu.popup(QCursor.pos())

    def __delete_item(self):
        self.rightClickSingal.emit(("delete", self.label))
