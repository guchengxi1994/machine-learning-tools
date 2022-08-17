import sys

sys.path.append("..")

from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget, QFileDialog
)
from PySide6.QtGui import QIcon, QAction
from PySide6 import QtCore

from components.custom_button import CustomButton


class MainScreen(QMainWindow):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.setWindowTitle("Machine learning tools")
        self.setWindowIcon(QIcon("assets/icon2.png"))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        layout = QHBoxLayout()

        self.__build_menubar()
        self.__build_left_side_toolbar()

        layout.addLayout(self.leftSideToolbar)

        layout.setAlignment(QtCore.Qt.AlignLeft)

        ## 窗口主体
        mainWidget = QWidget(self)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def __build_left_side_toolbar(self):
        self.leftSideToolbar = QVBoxLayout()
        self.openFileButton = CustomButton("Open file", "assets/file.png")
        self.openFileButton.clicked.connect(self.__open_file_func)
        self.leftSideToolbar.addWidget(self.openFileButton)
        self.leftSideToolbar.setAlignment(QtCore.Qt.AlignTop)

    def __open_file_func(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "选取一张图像", "./", 'Image files(*.jpg *.gif *.png)'
        )
        if filename != "":
            print(filename)

    def __build_menubar(self):
        menubar = self.menuBar()
        sysMenu = menubar.addMenu("&System")

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(self.close)
        sysMenu.addAction(exitAction)
