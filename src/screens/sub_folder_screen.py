from PySide6.QtWidgets import (
    QHBoxLayout,
    QStackedLayout,
    QDialog,
    QVBoxLayout,
    QFileDialog,
)
from PySide6.QtGui import QIcon
from PySide6 import QtCore
from components.file_management_widget import FileManagementWidget
from components.custom_button import CustomButton
from constants import *
from models import *


class SubFolderScreen(QDialog):
    def __init__(self, folder: Folder) -> None:
        super().__init__()
        self.folder = folder
        self.setWindowTitle(folder.folderName)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.folderList = [folder]
        stackLayout = QStackedLayout()
        self.fileManagementWidget = FileManagementWidget(self, canNavigate=False)
        stackLayout.addWidget(self.fileManagementWidget)
        self.__build_left_side_toolbar()

        layout = QHBoxLayout()
        layout.addLayout(self.leftSideToolbar)

        layout.addLayout(stackLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(layout)

    def __build_left_side_toolbar(self):
        self.leftSideToolbar = QVBoxLayout()
        self.openFileButton = CustomButton("Add File", ADD_FILE_ICON)
        self.openFileButton.clicked.connect(self.__open_file_func)

        self.backButton = CustomButton("Back", BACK_ICON)
        self.backButton.clicked.connect(self.__prev_func)

        self.leftSideToolbar.addWidget(self.openFileButton)
        self.leftSideToolbar.addWidget(self.backButton)
        self.leftSideToolbar.setAlignment(QtCore.Qt.AlignTop)

    def __prev_func(self):
        if len(self.folderList) == 1:
            return
        else:
            self.folderList.pop()
            # self.folder = self.folderList[-1]
            self.fileManagementWidget.repaintByParent()

    def __open_file_func(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择文件", "./")
        if filename != "":
            self.folderList[-1].append(File(filename))
            self.fileManagementWidget.repaintByParent()
