from components.base_toolbutton import BaseToolButton, FileOrFolder
from PySide6 import QtCore


class FolderElementWidget(BaseToolButton):
    def __init__(self, T: FileOrFolder, parent) -> None:
        super().__init__(T, parent)
        self.folder = T
        self.setToolTip("{} 包含{}个文件。".format(T.folderName, len(T.children)))

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)

        if e.buttons() == QtCore.Qt.RightButton:
            self.create_rightmenu()
            print("this is a folder :", self.label)
