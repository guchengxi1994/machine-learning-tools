from PySide6.QtWidgets import QToolButton
from PySide6 import QtCore
from PySide6.QtGui import QIcon


class CustomButton(QToolButton):
    def __init__(self, label: str, iconPath: str):
        super(CustomButton, self).__init__()
        self.setText(label)
        self.setIcon(QIcon(iconPath))
        self.setIconSize(QtCore.QSize(32, 32))
        self.setFixedWidth(80)
        self.setFixedHeight(70)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("padding-top: 20px;")
        