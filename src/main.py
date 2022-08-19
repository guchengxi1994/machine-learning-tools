import sys
from screens.main_screen import MainScreen
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainScreen = MainScreen()
    # mainScreen.show()

    sys.exit(app.exec())
