import subprocess
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
    ## 新窗口打开子文件夹
    navigateSingal = QtCore.Signal(Folder)

    def __init__(self, T: FileOrFolder, parent, canNavigate: bool = True) -> None:
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
        self.canNavigate = canNavigate

    def mousePressEvent(self, e) -> None:
        # print("start", self.pos())
        self.iniDragCor[0] = e.x()
        self.iniDragCor[1] = e.y()
        if type(self.T) is Folder:
            self.setIcon(QIcon(FOLDER_SELECTED_ICON))
        else:
            self.setIcon(QIcon(FOLDER_SELECTED_ICON))

    def mouseReleaseEvent(self, e) -> None:
        if type(self.T) is Folder:
            self.setIcon(QIcon(FOLDER_ICON))
        else:
            self.setIcon(QIcon(FILE_ICON))
        self.moveFileSingal.emit((self.pos().x(), self.pos().y(), self.label))

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

        if type(self.T) is Folder:
            if self.canNavigate:
                openInANewWindow = QAction(QIcon(NAVIGATE_ICON), "新窗口中打开", self)
                openInANewWindow.triggered.connect(self.__navigate)
                # print(type(self.parent))
                groupBoxMenu.addAction(openInANewWindow)

        if type(self.T) is File:
            secondMenu = groupBoxMenu.addMenu(QIcon(SECOND_MENU_ICON), "以...打开")
            txtOpenAction = QAction(QIcon(TXT_ICON), "以文本打开", self)
            txtOpenAction.triggered.connect(self.__open_with_txt)
            vscodeOpenAction = QAction(QIcon(VSCODE_ICON), "以vscode打开", self)
            vscodeOpenAction.triggered.connect(self.__open_with_vscode)
            # typoraOpenAction = QAction(QIcon(TYPORA_ICON), "以typora打开", self)
            secondMenu.addAction(txtOpenAction)
            secondMenu.addAction(vscodeOpenAction)
            # secondMenu.addAction(typoraOpenAction)

        groupBoxMenu.popup(QCursor.pos())
        if type(self.T) is Folder:
            self.setIcon(QIcon(FOLDER_ICON))
        else:
            self.setIcon(QIcon(FILE_ICON))

    def __delete_item(self):
        self.rightClickSingal.emit(("delete", self.label))

    def __navigate(self):
        self.navigateSingal.emit(self.T)
    
    def __open_with_txt(self):
        subprocess.Popen(["notepad",self.label],shell=True)
    
    # def __open_with_typora(self):
    #     ...

    def __open_with_vscode(self):
        subprocess.Popen(["code",self.label],shell=True)
        # os.system("code {}".format(self.label))
