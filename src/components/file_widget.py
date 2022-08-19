from components.base_toolbutton import BaseToolButton, FileOrFolder
from PySide6 import QtCore


class FileElementWidget(BaseToolButton):
    def __init__(self, T: FileOrFolder, parent) -> None:
        super().__init__(T, parent)
        self.setToolTip(T.fileName)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)

        if e.buttons() == QtCore.Qt.RightButton:
            self.create_rightmenu()
            print("this is a file :", self.label)
