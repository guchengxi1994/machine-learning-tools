from PySide6.QtWidgets import (
    QHBoxLayout,
    QStackedLayout,
    QDialog,
)
from PySide6.QtGui import QIcon
from PySide6 import QtCore
from components.file_management_widget import FileManagementWidget
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
        self.fileManagementWidget = FileManagementWidget(self)
        stackLayout.addWidget(self.fileManagementWidget)

        layout = QHBoxLayout()

        layout.addLayout(stackLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(layout)
