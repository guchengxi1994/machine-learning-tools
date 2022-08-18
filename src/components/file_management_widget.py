from typing import List
from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QToolButton, QMainWindow, QGridLayout

from models import Folder


class FileElementWidget(QToolButton):
    doubleClickSignal = QtCore.Signal(str)

    def __init__(self, label: str, parent):
        super().__init__(parent)
        self.setText(label)
        self.setIcon(QIcon("assets/file.png"))
        self.setIconSize(QtCore.QSize(32, 32))
        self.setFixedWidth(80)
        self.setFixedHeight(70)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("border : none")
        self.iniDragCor = [0, 0]
        self.label = label

    def mousePressEvent(self, e) -> None:
        # print("start", self.pos())
        self.iniDragCor[0] = e.x()
        self.iniDragCor[1] = e.y()

    def mouseReleaseEvent(self, e) -> None:
        # print("end", self.pos())
        ...

    def mouseDoubleClickEvent(self, event) -> None:
        self.doubleClickSignal.emit(self.label)

    def mouseMoveEvent(self, e) -> None:
        x = e.x() - self.iniDragCor[0]
        y = e.y() - self.iniDragCor[1]

        cor = QtCore.QPoint(x, y)
        self.move(self.mapToParent(cor))  # 需要maptoparent一下才可以的,否则只是相对位置。


class FolderElementWidget(QToolButton):
    doubleClickSignal = QtCore.Signal(str)

    def __init__(self, folder: Folder, parent):
        super().__init__(parent)
        self.setText(folder.folderName)
        self.setIcon(QIcon("assets/folder.png"))
        self.setIconSize(QtCore.QSize(32, 32))
        self.setFixedWidth(80)
        self.setFixedHeight(70)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("border : none")
        self.iniDragCor = [0, 0]
        self.folder = folder

    def mouseDoubleClickEvent(self, event) -> None:
        self.doubleClickSignal.emit(self.folder.folderName)

    def mousePressEvent(self, e) -> None:
        # print("start", self.pos())
        self.iniDragCor[0] = e.x()
        self.iniDragCor[1] = e.y()

    def mouseReleaseEvent(self, e) -> None:
        # print("end", self.pos())
        ...

    def mouseMoveEvent(self, e) -> None:
        x = e.x() - self.iniDragCor[0]
        y = e.y() - self.iniDragCor[1]

        cor = QtCore.QPoint(x, y)
        self.move(self.mapToParent(cor))  # 需要maptoparent一下才可以的,否则只是相对位置。


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
                f = FileElementWidget(i.fileName, self)
                f.doubleClickSignal.connect(self.__double_click_file)
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
